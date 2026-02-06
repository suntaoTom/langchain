import asyncio
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from agent.graph import graph

load_dotenv()

async def run_test():
    # Use a real request
    inputs = {
        "messages": [HumanMessage(content="Write a simple python script to hello world")],
        "iteration_count": 0,
        "project_root": os.path.abspath(".")
    }
    
    print("Invoking graph...")
    try:
        async for event in graph.astream(inputs):
            for node, state in event.items():
                print(f"\n--- Node: {node} ---")
                if "status" in state:
                    print(f"Status: {state['status']}")
                if "file_path" in state:
                    print(f"File Path: {state['file_path']}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(run_test())
