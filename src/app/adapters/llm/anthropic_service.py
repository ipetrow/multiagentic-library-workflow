import os

from anthropic import AnthropicFoundry
from pydantic import BaseModel

from src.app.tools.definitions.tool_definition import ToolDefinition

from .base_service import LLMService
from .models.llm_response import ToolUse
from .models.llm_response import LLMResponse
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
        
        self.anthropic = AnthropicFoundry(
            api_key=api_key,
            base_url=ENDPOINT
        )

        self.adapter = AnthropicContextMapper()
        self.context = []

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

        serialized_tools = await self._serialize_create_message_items(context_item, available_tools)

        request_params = await self._build_create_message(
            serialized_tools=serialized_tools, 
            system_prompt=system_prompt, 
            output_schema=output_schema
        )

        try:
            response = self.anthropic.messages.create(**request_params)
        except Exception as ex:
            print(f"Exception: {ex}")

        return await self._process_response(response)

    async def process_beta(
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

        serialized_tools = await self._serialize_create_message_items(context_item, available_tools)

        request_params = await self._build_create_beta_message(
            serialized_tools=serialized_tools,
            system_prompt=system_prompt, 
            output_schema=output_schema
        )

        try:
            response = self.anthropic.beta.messages.create(**request_params)
        except Exception as ex:
            print(f"Exception: {ex}")

        return await self._process_response(response)
        
    async def _serialize_create_message_items(
            self, 
            context_item: ContextItem | None = None, 
            available_tools: list[ToolDefinition] | None = None
        ) -> list[dict]:

        # serialize context
        item: ContextItem = None

        if isinstance(context_item, ContextRoleItem):
            item = await self.adapter.serialize_context_role_item(context_item)
        elif isinstance(context_item, ContextToolOutputItem):
            item = await self.adapter.serialize_context_tool_output_item(context_item)

        self.context.append(item)

        # serialize tools
        serialized_tools = await self.adapter.serialize_tools(available_tools) if available_tools else []

        return serialized_tools

    async def _process_response(self, response) -> LLMResponse:
        self.context.append(
            {
                "role": "assistant",
                "content": response.content
            }
        )

        tool_use: ToolUse = None
        assisstent_response_text = None

        # hadle all output items
        for content_item in response.content:
            
            # handle text/message if present
            if content_item.type == "text":
                assisstent_response_text = content_item.text
            elif content_item.type == "tool_use" and response.stop_reason == "tool_use": # handle a tool call request if present
                tool_use = ToolUse(
                    tool_name = content_item.name, 
                    tool_args = content_item.input,
                    call_id = content_item.id
                )

        return LLMResponse(
            response = assisstent_response_text, 
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
            "messages": self.context
        }

        if serialized_tools:
            request_params["tools"] = serialized_tools
            request_params["totool_choiceols"] = {"type": "auto", "disable_parallel_tool_use": True}

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
            system_prompt: str | None = None,
            output_schema: type[BaseModel] | None = None
    ) -> dict:
        request_params = {
            "model": MODEL,
            "max_tokens": MAX_TOKENS,
            "betas": ["code-execution-2025-08-25", "skills-2025-10-02"],
            "container": {
                "skills": [
                    {
                        "type": "custom", 
                        "skill_id": "skill_id", # TODO add the correct id
                        "version": "latest"
                    }
                ]
            },  
            "messages": self.context,
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