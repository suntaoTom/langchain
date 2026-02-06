"""Manager for MCP servers and tools integration."""

import logging
import os
import shlex
from contextlib import AsyncExitStack
from typing import List

from langchain_core.tools import BaseTool
from dotenv import load_dotenv
from langchain_mcp_adapters.tools import load_mcp_tools
from mcp import ClientSession, StdioServerParameters, stdio_client

# Load environment variables early, override existing to ensure .env takes precedence
load_dotenv(override=True)
logger = logging.getLogger(__name__)

class MCPManager:
    """Manager for MCP servers and tools integration. / MCP 服务器和工具集成的管理器。."""
    
    def __init__(self) -> None:
        """Initialize the MCP manager instance."""
        self.tools: List[BaseTool] = []
        self._initialized = False
        self._exit_stack = AsyncExitStack()
        
        # Debug: Check for Figma Key
        figma_key = os.getenv("FIGMA_API_KEY")
        if figma_key:
            logger.info("Found FIGMA_API_KEY in environment (length: %d)", len(figma_key))
        else:
            logger.warning("FIGMA_API_KEY NOT found in environment during MCPManager init")

    async def initialize_tools(self) -> None:
        """Discover and load tools from configured MCP servers and maintain connections. / 从配置的 MCP 服务器中发现并加载工具并维护连接。."""
        if self._initialized:
            return
        
        mcp_servers_env = os.getenv("MCP_SERVERS", "")
        if not mcp_servers_env:
            self._initialized = True
            return

        server_names = [s.strip() for s in mcp_servers_env.split(",")]
        all_tools = []

        for name in server_names:
            cmd_env = f"MCP_SERVER_{name.upper()}_CMD"
            cmd_str = os.getenv(cmd_env)
            
            if not cmd_str:
                logger.warning("Warning: No command found for MCP server %s (%s)", name, cmd_env)
                continue

            try:
                # Use shlex to correctly parse command strings with arguments
                parts = shlex.split(cmd_str)
                executable = parts[0]
                args = parts[1:]
                
                # Proactive fix for Figma: Ensure key is passed to the server
                if name.lower() == "figma":
                    figma_key = os.getenv("FIGMA_API_KEY")
                    if figma_key:
                        # Support @yhy2001/figma-mcp-server
                        if "@yhy2001/figma-mcp-server" in cmd_str and "--figma-api-key" not in args:
                             logger.info("Explicitly adding --figma-api-key")
                             args.extend(["--figma-api-key", figma_key])
                        # Support figma-developer-mcp or others using --api-key
                        elif "--api-key" not in args and "--figma-api-key" not in args:
                             logger.info("Explicitly adding --api-key")
                             args.extend(["--api-key", figma_key])

                server_params = StdioServerParameters(
                    command=executable,
                    args=args,
                    env=os.environ.copy()
                )
                
                # We use AsyncExitStack to keep the transport and session alive
                # transport is the context manager from stdio_client
                read, write = await self._exit_stack.enter_async_context(stdio_client(server_params))
                
                # session is the context manager from ClientSession
                session = await self._exit_stack.enter_async_context(ClientSession(read, write))
                
                # Important: initialize the session
                await session.initialize()
                
                # Now we can load tools from the initialized session
                tools = await load_mcp_tools(session)
                all_tools.extend(tools)
                logger.info("Loaded %d tools from MCP server: %s", len(tools), name)
                
            except Exception:
                logger.exception("Error loading MCP server %s", name)

        self.tools = all_tools
        self._initialized = True

    async def close_tools(self) -> None:
        """Close all MCP server connections. / 关闭所有 MCP 服务器连接。."""
        await self._exit_stack.aclose()
        self._initialized = False
        self.tools = []

    def get_tools(self) -> List[BaseTool]:
        """Return the list of loaded MCP tools. / 返回已加载 of MCP 工具列表。."""
        return self.tools

# Singleton instance
mcp_manager = MCPManager()
