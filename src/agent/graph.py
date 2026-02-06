"""Main graph definition for the software factory agent."""

from __future__ import annotations

from typing import Literal

from langgraph.graph import END, StateGraph

from agent.nodes import (
    analyzer_node,
    developer_node,
    mcp_node,
    pm_node,
    qa_node,
    writer_node,
)
from agent.state import FactoryState


def should_continue(state: FactoryState) -> Literal["developer_node", "writer_node", "__end__"]:
    """Determine next step based on QA status and iteration count. / 根据 QA 状态和迭代次数确定下一步。."""
    status = state["status"]
    iterations = state.get("iteration_count", 0)
    
    # If approved, move to writing the file / 如果审核通过，则开始写入文件
    if status == "approved":
        return "writer_node"
    
    # Deadlock prevention / 防止死锁: stop after 3 iterations
    if iterations >= 3:
        return END
    
    # Otherwise, keep retrying / 否则继续重试
    return "developer_node"

# Define the graph / 定义图
graph_builder = StateGraph(FactoryState)

# Add nodes / 添加节点
graph_builder.add_node("analyzer_node", analyzer_node)
graph_builder.add_node("mcp_node", mcp_node)
graph_builder.add_node("pm_node", pm_node)
graph_builder.add_node("developer_node", developer_node)
graph_builder.add_node("qa_node", qa_node)
graph_builder.add_node("writer_node", writer_node)

# Add edges / 添加边缘
graph_builder.add_edge("__start__", "analyzer_node")
graph_builder.add_edge("analyzer_node", "mcp_node")
graph_builder.add_edge("mcp_node", "pm_node")
graph_builder.add_edge("pm_node", "developer_node")
graph_builder.add_edge("developer_node", "qa_node")
graph_builder.add_edge("writer_node", END)

# Conditional edge from QA / 来自 QA 的条件边缘
graph_builder.add_conditional_edges(
    "qa_node",
    should_continue,
    {
        "developer_node": "developer_node",
        "writer_node": "writer_node",
        "__end__": END
    }
)

graph = graph_builder.compile()

# Explicitly export graph for LangGraph / 为 LangGraph 显式导出 graph
__all__ = ["graph"]
