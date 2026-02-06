"""Manager for MCP servers and tools integration."""

import logging
import os
from typing import List

from langchain_core.tools import BaseTool
from langchain_mcp_adapters.tools import load_mcp_tools
from mcp import StdioServerParameters

logger = logging.getLogger(__name__)

class MCPManager:
    """Manager for MCP servers and tools integration. / MCP 服务器和工具集成的管理器。."""
    
    def __init__(self):
        """Initialize the MCP manager instance."""
        self.tools: List[BaseTool] = []
        self._initialized = False

    async def initialize_tools(self):
        """Discover and load tools from configured MCP servers. / 从配置的 MCP 服务器中发现并加载工具。."""
        if self._initialized:
            return
        
        # Example configuration format in .env:
        # MCP_SERVERS = "figma,github"
        # MCP_SERVER_FIGMA_CMD = "npx -y @modelcontextprotocol/server-figma"
        # MCP_SERVER_GITHUB_CMD = "npx -y @modelcontextprotocol/server-github"
        
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
                # Basic command parsing (assumes space-separated)
                parts = cmd_str.split()
                executable = parts[0]
                args = parts[1:]
                
                server_params = StdioServerParameters(
                    command=executable,
                    args=args,
                    env=os.environ.copy()
                )
                
                # Note: load_mcp_tools is an async function in recent versions
                # It handles the context management internally or via a list of tools
                tools = await load_mcp_tools(server_params)
                all_tools.extend(tools)
                logger.info("Loaded %d tools from MCP server: %s", len(tools), name)
                
            except Exception:
                logger.exception("Error loading MCP server %s", name)

        self.tools = all_tools
        self._initialized = True

    def get_tools(self) -> List[BaseTool]:
        """Return the list of loaded MCP tools. / 返回已加载 of MCP 工具列表。."""
        return self.tools

# Singleton instance
mcp_manager = MCPManager()
