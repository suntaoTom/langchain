"""QA node for code review and approval."""

from typing import Any, Dict

from langchain_core.messages import HumanMessage, SystemMessage

from agent.factory_model import model
from agent.state import FactoryState


async def qa_node(state: FactoryState) -> Dict[str, Any]:
    """QA Agent: Reviews code against requirements and project guidelines. / QA Agent：根据需求和项目规范评审代码。."""
    requirements = state["requirements"]
    code = state["code"]
    project_guidelines = state.get("project_context", "")
    
    system_prompt = (
        "You are a Senior QA Engineer. "
        "Review the provided code stringently against the requirements, high-quality coding standards, "
        "and the project's AI-specific guidelines/rules. "
        "You MUST ensure the code adheres to any AI Rules or Skills documentation found in the project context."
    )
    
    user_prompt = (
        f"Project Guidelines/Rules (including AI Rules and Skills):\n{project_guidelines}\n\n"
        f"Requirements:\n{requirements}\n\n"
        f"Code:\n{code}\n\n"
        "Evaluate if the code meets all requirements, adheres to the guidelines, and is of high quality. "
        "If you approve it, you must clearly state 'APPROVED' in your response."
    )
    
    is_approved = False
    feedback = ""
    
    try:
        response = await model.ainvoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])
        
        content = response.content if hasattr(response, "content") else str(response)
        
        # More robust approval check / 更健壮的批准检查
        if "APPROVED" in content.upper():
            is_approved = True
            feedback = "Approved."
        else:
            is_approved = False
            feedback = content

    except Exception as e:
        is_approved = False
        feedback = f"QA evaluation error: {str(e)}"

    status = "approved" if is_approved else "revision"
    response_msg = HumanMessage(content=f"QA Result: {status.upper()}\nFeedback: {feedback}")
        
    return {
        "feedback": feedback,
        "messages": [response_msg],
        "status": status
    }
