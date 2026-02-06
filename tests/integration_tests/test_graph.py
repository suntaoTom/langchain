import pytest
from langchain_core.messages import HumanMessage
from agent import graph

pytestmark = pytest.mark.anyio


@pytest.mark.langsmith
async def test_agent_simple_passthrough() -> None:
    inputs = {
        "messages": [HumanMessage(content="Write a simple python script to hello world")],
        "iteration_count": 0
    }
    res = await graph.ainvoke(inputs)
    assert res is not None
    assert "messages" in res
    assert len(res["messages"]) > 0
