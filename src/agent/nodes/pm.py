import re
from typing import Any, Dict
from langchain_core.messages import HumanMessage, SystemMessage
from agent.state import FactoryState
from agent.utils import get_last_message_content
from agent.factory_model import model

async def pm_node(state: FactoryState) -> Dict[str, Any]:
    """Product Manager Agent: Converts user requests into detailed requirements using project context. / 产品经理 Agent：利用项目上下文将用户请求转换为详细的需求文档。"""
    user_request = get_last_message_content(state["messages"])
    project_map = state.get("project_map", "Unknown structure")
    project_guidelines = state.get("project_context", "")
    
    system_prompt = (
        "You are an experienced Product Manager. "
        "Your goal is to convert user requests into a detailed Requirements Document. "
        "You MUST carefully read and adhere to all AI-specific rules, guidelines, and skills documentation found in the project context."
    )
    
    prompt = (
        f"Project Structure:\n{project_map}\n\n"
        f"Project Guidelines/Rules (including AI Rules and Skills):\n{project_guidelines}\n\n"
        f"User Request: {user_request}\n\n"
        "1. Analyze the request and create a detailed Requirements Document (Goal, Functional, Acceptance).\n"
        "2. Based on the Project Guidelines and Structure, determine the most appropriate programming language and framework.\n"
        "3. Identify the best 'file_path' to save this new code within the existing structure. "
        "The path MUST be relative to the project root (e.g., 'app/pages/NewPage.tsx'). "
        "Do NOT include the project root directory name in the path itself. "
        "Format your response to include a clearly labeled 'FILE_PATH: path/to/file.extension' line."
    )
    
    response = await model.ainvoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=prompt)
    ])
    
    content = response.content
    suggested_path = None
    if "FILE_PATH:" in content:
        match = re.search(r"FILE_PATH:\s*([^\s\n]+)", content)
        if match:
            suggested_path = match.group(1)
            
    return {
        "requirements": content,
        "file_path": suggested_path,
        "messages": [response],
        "iteration_count": 0,
        "status": "requirements_defined"
    }
