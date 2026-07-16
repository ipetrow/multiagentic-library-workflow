from contextlib import AsyncExitStack
import json
import os

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from .models.models import ToolCallResponse

class MCPManager:

    def __init__(self):
        self.exit_stack = AsyncExitStack()
        self._sessions = {}

    async def __aenter__(self):
        await self._connect_to_servers()
        return self
    
    async def __aexit__(self, *_):
        await self.exit_stack.aclose()

    async def _connect_to_server(self, server_name, server_config) -> ClientSession:
        """
        Established a MCP Client-Server connection.

        Args:
            server_name: the name of the server to which a connection will be stablished.
            server_config: the server configuration information used for connecting to the server.
        
        Returns:
            A client session.
        """
        try:
            server_params = StdioServerParameters(**server_config)
            stdio_transport = await self.exit_stack.enter_async_context(
                stdio_client(server_params)
            )
            self.stdio, self.write = stdio_transport
            session = await self.exit_stack.enter_async_context(
                ClientSession(self.stdio, self.write)
            )

            await session.initialize()

            self._sessions[server_name] = session
            await self._notify_server_connection_successful(server_name, session)

            return session
        except Exception as e:
            raise RuntimeError(f"Error trying to connect to MCP Server {server_name}: {e}")
    
    async def _connect_to_servers(self):
        """Reads the server configuration files and established all the MCP Client-Server connections."""

        try:
            with open("src/agent/api/mcp.json", "r") as file:
                data = json.load(file)
            servers = data.get("servers", {})
            for server_name, server_config in servers.items():
                server_config_updated = await self._resolve_server_config(server_config)
                await self._connect_to_server(server_name, server_config_updated)
        except Exception as e:
            raise RuntimeError(f"Error loading the server configuration file: {e}")

    async def get_tools(self) -> list:
        """
        Returns a list of all the tools available in all the started client sessions. 

        Returns:
            A list of all the available tools.
        """

        available_tools = []

        for session_name, session in self._sessions.items():
            tools_response = await session.list_tools()

            for tool in tools_response.tools:
                available_tools.append(
                    {
                        "session_name": session_name,
                        "tool": tool
                    }
                )

        return available_tools
    
    async def call_tool(self, session_name: str, tool_name: str, tool_args) -> ToolCallResponse:
        """
        Executes a tool by specified name and arguments.
        
        Args:
            session_name: The name of the session to which the tool belongs.
            tool_name: The name of the tool that will be executed.
            tool_args: The required arguments of the tool that will be executed.
        Returns:
            The tool response - the content and logs.
        """

        await self._assert_tool_available(session_name = session_name, tool_name = tool_name)

        session = await self._get_session(session_name)

        try:
            log = f"[Log: Calling tool with name = {tool_name} and args = {tool_args}]]"
            result = await session.call_tool(tool_name, tool_args)
            content = result.content[0].text if result.content else ""
        except Exception as e:
            content = f"Error: {e}"
            log = f"[{content}]"

        return ToolCallResponse(content = content, log = log)
    
    async def get_resource(self, session_name: str, resource_uri: str) -> str:
        """
        Gets the content of a receipt pdf file as a base64 encoded string.
        
        Args:
            session_name: The name of the session to which the resource belongs.
            resource_uri: a resource uri exposed from the mcp-server for a specific resource.

        Returns: the content of the pdf file in a base64 encoded string.
        """

        await self._assert_resource_available(session_name = session_name, resource_uri = resource_uri)

        session = await self._get_session(name = session_name)
        
        try:
            print(f"\nRequesting the resource: {resource_uri}")
            result = await session.read_resource(uri=resource_uri)
            if result and result.contents:
                return result.contents[0].text
            else:
                print("No content available.")
        except Exception as e:
            print(f"Error: {e}")

    async def _assert_tool_available(self, session_name: str, tool_name: str):
        session = await self._get_session(name = session_name)
        available_tools_response = await session.list_tools()

        available_tool_names = [
            tool.name
            for tool in available_tools_response.tools
        ]

        if tool_name not in available_tool_names:
            raise ValueError(f"No tool with name {tool_name} is available for session {session_name}")
        
    async def _assert_resource_available(self, session_name: str, resource_uri: str):
        session = await self._get_session(name = session_name)
        available_resources_response = await session.list_resources()

        available_resource_uris = [
            str(resource.uri) # getting the uri as a str from an AnyUrl object
            for resource in available_resources_response.resources
        ]

        if resource_uri not in available_resource_uris:
            raise ValueError(f"No resource with uri {resource_uri} is available for session {session_name}")

    async def _get_session(self, name: str) -> ClientSession:
        """
        Returns the corresponding session to the specified server primitive item type (tool, resource).

        Args:
            name: The session name.

        Returns:
            A client session.
        """

        session = self._sessions[name]

        if not session:
            raise ValueError(f"No session found for {name}")
        
        return session
        
    async def _notify_server_connection_successful(self, server_name, session):
        """
        Notifies when a successful connection to a server is established by listing all its available primitives.

        Args:
            server_name: The sever name to which a connection is established.
            session: The client session corresponding to the server.
        """

        print(f"\n- MCP Server: {server_name} successfully connected")

        try:
            tools_response = await session.list_tools()
            if tools_response and tools_response.tools:
                print("----- Tools: ", [tool.name for tool in tools_response.tools])

            resources_response = await session.list_resources()
            if resources_response and resources_response.resources:
                print(f"----- Resources: ", [resource.name for resource in resources_response.resources])

            prompts_response = await session.list_prompts()
            if prompts_response and prompts_response.prompts:
                print(f"----- Prompts: ", [prompt.name for prompt in prompts_response.prompts])
        except Exception as e:
            print(f"Error {e}")

    async def _resolve_server_config(self, server_config: dict) -> dict:
        config = server_config.copy()

        env = {}

        for key, value in config.get("env", {}).items():
            if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                env_variable_name = value[2:-1]

                try:
                    env[key] = os.environ[env_variable_name]
                except KeyError:
                    raise RuntimeError(
                        f"Required environment variable '{env_variable_name}' is missing."
                    )
            else:
                env[key] = value

        if env:
            config["env"] = env

        return config