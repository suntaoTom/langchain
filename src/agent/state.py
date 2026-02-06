import operator
from typing import List, Optional, Annotated, TypedDict
from langchain_core.messages import AnyMessage

class FactoryState(TypedDict):
    """The state of the software factory. / 软件工厂的状态。"""
    # Conversation history / 对话历史
    messages: Annotated[List[AnyMessage], operator.add]
    # Artifacts / 中间产物
    requirements: Optional[str]
    code: Optional[str]
    feedback: Optional[str]
    file_path: Optional[str]  # Target path for the generated code / 生成代码的目标路径
    project_map: Optional[str] # Context of the existing project structure / 现有项目结构的上下文
    project_root: Optional[str] # Root directory to analyze / 要分析的根目录
    project_context: Optional[str] # Content of AI instructions/guidelines / AI 指导/规范文件的内容
    design_data: Optional[str] # Data retrieved from design tools (e.g. Figma) via MCP / 通过 MCP 从设计工具（如 Figma）检索的数据
    # Process control / 过程控制
    iteration_count: int
    status: str
