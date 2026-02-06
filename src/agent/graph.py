from __future__ import annotations
from typing import Literal
from langgraph.graph import StateGraph, END
from agent.state import FactoryState
from agent.nodes import (
    analyzer_node,
    pm_node,
    developer_node,
    qa_node,
    writer_node
)

def should_continue(state: FactoryState) -> Literal["developer_node", "writer_node"]:
    """Determine next step based on QA status. / 根据 QA 状态确定下一步。"""
    status = state["status"]
    
    # If approved, move to writing the file / 如果审核通过，则开始写入文件
    if status == "approved":
        return "writer_node"
    
    # Otherwise, keep retrying indefinitely until approved / 否则持续重试直至审核通过
    return "developer_node"

# Define the graph / 定义图
graph_builder = StateGraph(FactoryState)

# Add nodes / 添加节点
graph_builder.add_node("analyzer_node", analyzer_node)
graph_builder.add_node("pm_node", pm_node)
graph_builder.add_node("developer_node", developer_node)
graph_builder.add_node("qa_node", qa_node)
graph_builder.add_node("writer_node", writer_node)

# Add edges / 添加边缘
graph_builder.add_edge("__start__", "analyzer_node")
graph_builder.add_edge("analyzer_node", "pm_node")
graph_builder.add_edge("pm_node", "developer_node")
graph_builder.add_edge("developer_node", "qa_node")
graph_builder.add_edge("writer_node", END)

# Conditional edge from QA / 来自 QA 的条件边缘
graph_builder.add_conditional_edges(
    "qa_node",
    should_continue,
    {
        "developer_node": "developer_node",
        "writer_node": "writer_node"
    }
)

graph = graph_builder.compile()

# Explicitly export graph for LangGraph / 为 LangGraph 显式导出 graph
__all__ = ["graph"]
