"""Analyzer node for project structural and guideline analysis."""

import asyncio
import os
from typing import Any, Dict

from agent.state import FactoryState
from agent.utils import get_project_structure, read_project_guidelines


async def analyzer_node(state: FactoryState) -> Dict[str, Any]:
    """Analyzer Agent: Scans project structure AND reads AI guidelines. / 分析器 Agent：扫描项目结构并读取 AI 指导规范。."""
    root_dir = state.get("project_root") or os.getenv("PROJECT_ROOT", ".")
    
    project_map, project_context = await asyncio.gather(
        asyncio.to_thread(get_project_structure, root_dir),
        asyncio.to_thread(read_project_guidelines, root_dir)
    )
    
    return {
        "project_map": project_map,
        "project_context": project_context,
        "project_root": root_dir,
        "status": "project_analyzed"
    }
