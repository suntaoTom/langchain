"""State definition for the software factory agent."""

import operator
from typing import Annotated, List, Union

from langchain_core.messages import AnyMessage
from typing_extensions import TypedDict


class FactoryState(TypedDict):
    """The state of the software factory. / 软件工厂的状态。."""

    # Conversation history / 对话历史
    messages: Annotated[List[AnyMessage], operator.add]
    # Artifacts / 中间产物
    requirements: Union[str, None]
    code: Union[str, None]
    feedback: Union[str, None]
    file_path: Union[str, None]  # Target path for the generated code / 生成代码的目标路径
    project_map: Union[str, None] # Context of the existing project structure / 现有项目结构的上下文
    project_root: Union[str, None] # Root directory to analyze / 要分析的根目录
    project_context: Union[str, None] # Content of AI instructions/guidelines / AI 指导/规范文件的内容
    design_data: Union[str, None] # Data retrieved from design tools (e.g. Figma) via MCP / 通过 MCP 从设计工具（如 Figma）检索的数据
    # Process control / 过程控制
    iteration_count: int
    status: str
