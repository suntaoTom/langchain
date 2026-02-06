"""MCP node for fetching external design data (e.g. Figma)."""

import re
from typing import Any, Dict

from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

from agent.factory_model import model
from agent.mcp_manager import mcp_manager
from agent.state import FactoryState
from agent.utils import get_last_message_content


async def mcp_node(state: FactoryState) -> Dict[str, Any]:
    """MCP Agent: Uses MCP tools to fetch external context (e.g. Figma designs). / MCP Agent：使用 MCP 工具获取外部上下文（例如 Figma 设计）。."""
    user_request = get_last_message_content(state.get("messages", []))
    
    # Quick check: does the request contain a URL?
    urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', user_request)
    if not urls:
        return {"status": "mcp_skipped"}

    # Initialize MCP tools if not already done
    await mcp_manager.initialize_tools()
    tools = mcp_manager.get_tools()
    
    if not tools:
        return {"status": "mcp_no_tools"}

    # Bind tools to the model
    model_with_tools = model.bind_tools(tools)
    
    system_prompt = (
        "You are a Design System Specialist. Your task is to extract design information from external sources like Figma. "
        "Use the provided MCP tools to fetch data from any URLs mentioned in the user request. "
        "Summarize the visual design, layout, colors, and components in a way that is useful for a developer."
    )
    
    # We might need multiple turns for tool execution
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"User request: {user_request}\nPlease use the tools to analyze any design URLs and provide a detailed summary.")
    ]
    
    response = await model_with_tools.ainvoke(messages)
    messages.append(response)
    
    # Check if there are tool calls
    if response.tool_calls:
        # For simplicity in this node, we'll execute the tool calls and get one more response
        # In a full LangGraph, this would be a cycle, but here we keep it direct
        for tool_call in response.tool_calls:
            # Find the tool
            tool_name = tool_call["name"]
            tool_to_use = next((t for t in tools if t.name == tool_name), None)
            
            if tool_to_use:
                try:
                    tool_result = await tool_to_use.ainvoke(tool_call["args"])
                    messages.append(ToolMessage(content=str(tool_result), tool_call_id=tool_call["id"]))
                except Exception as e:
                    messages.append(ToolMessage(content=f"Error executing tool: {str(e)}", tool_call_id=tool_call["id"]))
            else:
                messages.append(ToolMessage(content=f"Tool {tool_name} not found.", tool_call_id=tool_call["id"]))
        
        # Get the final summary from the LLM
        final_response = await model_with_tools.ainvoke(messages)
        design_summary = final_response.content
    else:
        design_summary = response.content

    return {
        "design_data": design_summary,
        "status": "design_analyzed",
        "messages": [HumanMessage(content=f"[Design Analysis Summary]: {design_summary}")]
    }
