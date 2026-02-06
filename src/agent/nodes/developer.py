"""Developer node for code generation based on requirements."""

from typing import Any, Dict

from langchain_core.messages import HumanMessage, SystemMessage

from agent.factory_model import model
from agent.state import FactoryState


async def developer_node(state: FactoryState) -> Dict[str, Any]:
    """Developer Agent: Writes code based on requirements and project context. / 开发人员 Agent：根据需求和项目上下文编写代码。."""
    requirements = state.get("requirements")
    feedback = state.get("feedback")
    project_map = state.get("project_map", "")
    project_guidelines = state.get("project_context", "")
    design_data = state.get("design_data", "")
    
    system_prompt = (
        "You are a Senior Software Engineer. "
        "Write clean, efficient code that follows the existing project's conventions, language, and AI guidelines. "
        "You MUST strictly follow any AI-related rules or specialized 'skills' documented in the project context. "
        "If design data (e.g., from Figma) is available, ensure the code implementation matches the design exactly."
    )
    
    user_prompt = (
        f"Project Context Structure:\n{project_map}\n\n"
        f"Project Guidelines/Rules:\n{project_guidelines}\n\n"
        f"Design Context (from MCP/Figma):\n{design_data}\n\n"
        f"Requirements:\n{requirements}\n\n"
    )
    
    if feedback:
        user_prompt += (
            f"QA Feedback from previous attempt:\n{feedback}\n\n"
            "Please rewrite the code to fix the issues mentioned. Return ONLY the code content."
        )
    else:
        user_prompt += "Please write the code to satisfy these requirements. Return ONLY the code content."
        
    response = await model.ainvoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ])
    
    return {
        "code": response.content,
        "messages": [response],
        "iteration_count": state.get("iteration_count", 0) + 1,
        "status": "code_written"
    }
