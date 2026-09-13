import os

from anthropic import AnthropicFoundry
from pydantic import BaseModel

from src.app.skills.models import Skill
from src.app.tools.definitions.tool_definition import ToolDefinition

from .base_service import LLMService
from .models.llm_response import ToolUse
from .models.llm_response import LLMResponse, LLMUsage
from .models.models import ContextRoleItem, ContextItem, ContextToolOutputItem
from .anthropic_mapper import AnthropicContextMapper

MODEL = "" # TODO add respective model name
MAX_TOKENS = 1000
ENDPOINT = "" # TODO add azure endpoint

class AnthropicService(LLMService):
    """Handles the communication between the Anthropic Claude Message API and the MCP tool execution."""

    def __init__(self):
        api_key = os.getenv("AZURE_ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError(
                "AZURE_ANTHROPIC_API_KEY environment variable is empty."
            )
        
        self._anthropic = AnthropicFoundry(
            api_key=api_key,
            base_url=ENDPOINT
        )

        self._adapter = AnthropicContextMapper()
        self._context = []

    async def process(
            self, 
            system_prompt: str,
            context_item: ContextItem | None = None, 
            available_tools: list[ToolDefinition] | None = None,
            output_schema: type[BaseModel] | None = None
        ) -> LLMResponse:
        """
        Handles a request to the Anthropic Claude Message API.

        Args:
            context_item: the context item which will be appened to the context history (contains e.g., prompt, tools response).
            available_tools: the available tools the execution of which the LLM might request.

        Returns:
            The response from the Anthropic request.
        """

        serialized_context_item = await self._serialize_context_item(context_item)
        self._context.append(serialized_context_item)
        serialized_tools = await self._adapter.serialize_tools(available_tools) if available_tools else []

        request_params = await self._build_create_message(
            serialized_tools=serialized_tools, 
            system_prompt=system_prompt, 
            output_schema=output_schema
        )

        try:
            response = self._anthropic.messages.create(**request_params)
        except Exception as ex:
            print(f"Exception: {ex}")

        return await self._process_response(response)

    async def process_beta(
            self, 
            system_prompt: str,
            skills: list[Skill] | None = None,
            context_item: ContextItem | None = None, 
            available_tools: list[ToolDefinition] | None = None,
            output_schema: type[BaseModel] | None = None
        ) -> LLMResponse:
        """
        Handles a request to the Anthropic Claude Message API.

        Args:
            context_item: the context item which will be appened to the context history (contains e.g., prompt, tools response).
            available_tools: the available tools the execution of which the LLM might request.

        Returns:
            The response from the Anthropic request. 
        """

        serialized_context_item = await self._serialize_context_item(context_item)
        self._context.append(serialized_context_item)
        serialized_tools = await self._adapter.serialize_tools(available_tools) if available_tools else []
        serialized_skills = await self._adapter.serialize_skills(skills) if skills else []

        request_params = await self._build_create_beta_message(
            serialized_tools=serialized_tools,
            system_prompt=system_prompt, 
            output_schema=output_schema,
            serialized_skills=serialized_skills
        )

        try:
            response = self._anthropic.beta.messages.create(**request_params)
        except Exception as ex:
            print(f"Exception: {ex}")

        return await self._process_response(response)
        
    async def _serialize_context_item(
            self, 
            context_item: ContextItem | None = None
        ) -> dict:

        if isinstance(context_item, ContextRoleItem):
            return await self._adapter.serialize_context_role_item(context_item)
        elif isinstance(context_item, ContextToolOutputItem):
            return await self._adapter.serialize_context_tool_output_item(context_item)

    async def _process_response(self, response) -> LLMResponse:
        self._context.append(
            {
                "role": "assistant",
                "content": response.content
            }
        )

        tool_use: ToolUse = None
        content_item_texts = []

        # hadle all output items
        for content_item in response.content:
            
            # handle text/message if present
            if content_item.type == "text":
                content_item_texts.append(content_item.text)
            elif content_item.type == "tool_use" and response.stop_reason == "tool_use": # handle a tool call request if present
                tool_use = ToolUse(
                    tool_name = content_item.name, 
                    tool_args = content_item.input,
                    call_id = content_item.id
                )

        assisstent_response_text = "\n".join(content_item_texts)

        return LLMResponse(
            call_id = response.id,
            response = assisstent_response_text, 
            usage=LLMUsage(
                input_tokens=response.usage.input_tokens, 
                output_tokens=response.usage.output_tokens
            ),
            tool_use = tool_use
        )

    async def _build_create_message(
            self,
            serialized_tools: list[dict],
            system_prompt: str | None = None,
            output_schema: type[BaseModel] | None = None
    ) -> dict:
        request_params = {
            "model": MODEL,
            "max_tokens": MAX_TOKENS, 
            "messages": self._context
        }

        if serialized_tools:
            request_params["tools"] = serialized_tools
            request_params["tool_choice"] = {"type": "auto", "disable_parallel_tool_use": True}

        request_params = await self._add_system_prompt_param(
            request_params=request_params, 
            system_prompt=system_prompt
        )
        request_params = await self._add_output_schema_param(
            request_params=request_params, 
            output_schema=output_schema
        )

        return request_params

    async def _build_create_beta_message(
            self,
            serialized_tools: list[dict],
            serialized_skills: list[dict],
            system_prompt: str | None = None,
            output_schema: type[BaseModel] | None = None,
    ) -> dict:
        request_params = {
            "model": MODEL,
            "max_tokens": MAX_TOKENS,
            "betas": ["code-execution-2025-08-25", "skills-2025-10-02"],
            "container": {
                "skills": serialized_skills
            },  
            "messages": self._context,
            "tools": serialized_tools + [{"type": "code_execution_20250825", "name": "code_execution"}],
            "tool_choice": {"type": "auto", "disable_parallel_tool_use": True},
        }

        request_params = await self._add_system_prompt_param(
            request_params=request_params, 
            system_prompt=system_prompt
        )
        request_params = await self._add_output_schema_param(
            request_params=request_params, 
            output_schema=output_schema
        )

        return request_params

    async def _add_system_prompt_param(self, request_params: dict, system_prompt: str | None = None) -> dict:

        if system_prompt is not None:
            request_params["system"] = system_prompt
        return request_params

    async def _add_output_schema_param(self, request_params: dict, output_schema: type[BaseModel] | None = None) -> dict:

        if output_schema is not None:
            request_params["output_config"] = {
                "format": {
                    "type": "json_schema",
                    "schema": output_schema.model_json_schema()
                }
            }
        return request_params