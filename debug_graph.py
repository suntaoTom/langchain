"""Debug script to run the graph locally and inspect node events."""

import asyncio
import logging
import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

from agent.graph import graph

load_dotenv()
logger = logging.getLogger(__name__)

async def run_test():
    """Run a simple test of the graph."""
    # Use a real request
    inputs = {
        "messages": [HumanMessage(content="Write a simple python script to hello world")],
        "iteration_count": 0,
        "project_root": os.path.abspath(".")
    }
    
    logger.info("Invoking graph...")
    try:
        async for event in graph.astream(inputs):
            for node, state in event.items():
                logger.info("\n--- Node: %s ---", node)
                if "status" in state:
                    logger.info("Status: %s", state["status"])
                if "file_path" in state:
                    logger.info("File Path: %s", state["file_path"])
    except Exception:
        logger.exception("Error while running graph")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run_test())
