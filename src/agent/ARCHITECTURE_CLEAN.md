# AI 软件工厂架构文档 (AI Software Factory Architecture)

本文档描述了 `src/agent` 目录下重构后的模块化结构。

## 目录结构 (Directory Structure)

```text
src/agent/
├── graph.py             # 图定义 (Graph Definition) - 核心入口，定义节点连接和流程控制
├── state.py             # 状态定义 (State Definition) - 定义 FactoryState 结构
├── utils.py             # 工具函数 (Utilities) - 包含文件扫描、文档读取、路径处理等通用逻辑
├── model_config.py      # 模型基础配置 (Model Config) - 多模型提供者（Gemini, Qwen 等）的工厂类
├── factory_model.py     # 模型实例 (Factory Model) - 为 Graph 节点提供统一的模型实例
└── nodes/               # 角色节点 (Agent Nodes) - 各个角色的原子逻辑
    ├── __init__.py      # 包初始化 (Package Init)
    ├── analyzer.py      # 分析器 (Analyzer) - 扫描项目结构和 AI 指导规范 (Rules/Skills)
    ├── pm.py            # 产品经理 (PM) - 解析需求并确定文件路径
    ├── developer.py     # 开发人员 (Developer) - 编写符合规范的代码
    ├── qa.py            # 质量保证 (QA) - 评审代码质量和规范符合度
    └── writer.py        # 文件写入 (Writer) - 将通过评审的代码保存至本地文件系统
```

## 核心模块说明 (Core Modules)

### 1. `graph.py`
使用 LangGraph 定义状态机。它不包含具体的业务逻辑，仅负责将各个 `nodes` 连接起来，并定义条件跳转逻辑（如 QA 未通过则返回 Developer）。

### 2. `state.py`
定义了 `FactoryState`。这是在所有节点之间传递的唯一数据载体，包含：
- `messages`: 对话历史。
- `requirements`: PM 生成的需求文档。
- `code`: Developer 生成的代码。
- `project_context`: 自动加载的 AI 规则和技能文档内容。
- `file_path`: 目标保存路径。

### 3. `utils.py`
集中管理阻塞型 I/O 和计算逻辑：
- `get_project_structure`: 生成项目树状图。
- `read_project_guidelines`: **关键逻辑**，负责自动搜索以 `AI` 或 `ai` 开头的规则文件或技能目录，并递归读取其内容。
- `save_file_sync`: 确保以标准方式写入文件。

### 4. `nodes/` 文件夹
每个文件代表链条中的一个工作环节。这种拆分方式使得我们可以针对性地优化某个角色的 Prompt 或逻辑（例如，可以给 `developer.py` 增加更具体的代码补全策略），而不会影响其他部分。

## 工作流程 (Workflow)

1.  **Analyzer**: 启动时先“学习”项目。它读取项目结构并自动提取所有 AI 相关的指令文档（Rules & Skills）。
2.  **PM**: 基于用户请求和 Analyzer 提供的内容，输出详细需求并指定相对路径。
3.  **Developer**: 根据需求和 AI 规范编写代码。
4.  **QA**: 进行严苛评审。如果代码不符合项目里的 AI 规范，将打回重写。
5.  **Writer**: 仅在 QA `APPROVED` 后，将代码安全地写入本地磁盘。

---
*注：该架构旨在提高 AI 在特定项目环境下的“感知能力”和“合规性”。*
