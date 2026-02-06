"""State definition for the software factory agent."""

import operator
from typing import Annotated, List, TypedDict

from langchain_core.messages import AnyMessage


class FactoryState(TypedDict):
    """The state of the software factory. / 软件工厂的状态。."""

    # Conversation history / 对话历史
    messages: Annotated[List[AnyMessage], operator.add]
    # Artifacts / 中间产物
    requirements: str | None
    code: str | None
    feedback: str | None
    file_path: str | None  # Target path for the generated code / 生成代码的目标路径
    project_map: str | None # Context of the existing project structure / 现有项目结构的上下文
    project_root: str | None # Root directory to analyze / 要分析的根目录
    project_context: str | None # Content of AI instructions/guidelines / AI 指导/规范文件的内容
    design_data: str | None # Data retrieved from design tools (e.g. Figma) via MCP / 通过 MCP 从设计工具（如 Figma）检索的数据
    # Process control / 过程控制
    iteration_count: int
    status: str
