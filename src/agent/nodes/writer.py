import os
import re
import asyncio
from typing import Any, Dict
from langchain_core.messages import SystemMessage
from agent.state import FactoryState
from agent.utils import save_file_sync

async def writer_node(state: FactoryState) -> Dict[str, Any]:
    """File Writer Agent: Saves the generated code to the local filesystem. / 文件写入 Agent：将生成的代码保存到本地文件系统。"""
    code = state["code"] or ""
    
    # Use PM's suggested path or fallback to a default
    suggested_path = state.get("file_path") or "output/generated_code.txt"
    project_root = state.get("project_root") or "."
    
    # Path normalization logic / 路径规范化逻辑:
    root_abs = os.path.abspath(project_root)
    root_name = os.path.basename(root_abs)
    
    clean_suggested = suggested_path.lstrip("/")
    
    path_parts = clean_suggested.split(os.sep)
    if path_parts[0] == root_name and len(path_parts) > 1:
        clean_suggested = os.sep.join(path_parts[1:])
    
    file_path = os.path.join(root_abs, clean_suggested)
    
    # Cleaning code from markdown blocks
    clean_code = re.sub(r"```[a-zA-Z]*\n?", "", code).replace("```", "").strip()
    
    try:
        await asyncio.to_thread(save_file_sync, file_path, clean_code)
        status = "file_saved"
        msg = f"Successfully saved code to {file_path}. / 成功将代码保存至 {file_path}。"
    except Exception as e:
        status = "error"
        msg = f"Failed to save file to {file_path}: {str(e)} / 无法将文件保存至 {file_path}：{str(e)}"
        
    return {
        "status": status,
        "messages": [SystemMessage(content=msg)]
    }
