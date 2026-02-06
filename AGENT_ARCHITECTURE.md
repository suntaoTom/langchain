# LangGraph 多智能体协同开发架构说明 (Agent Architecture)

本文档对 `src/agent/graph.py` 脚本实现的自动化软件开发工作流进行了详细解读。

## 1. 核心架构设计

该脚本利用 **LangGraph** 实现了一个闭环的自动化开发流程，模拟了真实开发团队中 **产品经理 (PM)**、**开发人员 (Developer)**、**测试工程师 (QA)** 以及 **文件写入器 (Writer)** 四个角色的协作逻辑。

### 角色分配与职责
| 智能体 | 角色 | 主要职责 |
| :--- | :--- | :--- |
| **PM Node** | 产品经理 | 解析用户请求，将其转化为包含目标、功能和验收标准的详细需求文档。 |
| **Developer Node** | 高级 Python 开发 | 根据需求编写代码；若收到 QA 反馈，则根据反馈修复 Bug 并重写代码。 |
| **QA Node** | 资深测试工程师 | 评估代码是否完全符合需求及高质量标准。输出结构化的评审结果。 |
| **Writer Node** | 文件写入器 | **(新增)** 在 QA 审核通过后，负责将生成的纯净代码保存到指定的本地项目路径。 |

---

## 2. 状态管理 (`FactoryState`)

整个流程共享一个状态字典，用于在不同节点间传递上下文和中间产物：

*   `messages`: 完整的对话消息历史。
*   `requirements`: PM 生成的需求文档。
*   `code`: Developer 生成的代码字符串。
*   `feedback`: QA 提供的修改意见（仅在发生修订时存在）。
*   `file_path`: **(新增)** 目标文件存储路径。若未提供，默认为 `output/generated_code.py`。
*   `iteration_count`: 记录开发迭代次数，用于防止陷入死循环。
*   `status`: 流程当前所处的状态标志位。

---

## 3. 工作流逻辑 (Workflow Logic)

### 流程图描述
1.  **开始 (`__start__`)** -> `pm_node`: 初始化并定义需求。
2.  **需求定义** -> `developer_node`: 编写第一版代码。
3.  **代码提交** -> `qa_node`: 进行代码质量与需求对齐审核。
4.  **决策分支 (`should_continue`)**:
    *   **审核通过 (APPROVED)**: 进入 `writer_node` 进行文件持久化。
    *   **需要修改 (REVISION NEEDED)**: 检查迭代次数。若小于 3 次，跳回 `developer_node`；否则强制终止。
5.  **文件保存 (`writer_node`)** -> **结束 (`__end__`)**: 代码写入磁盘后完成任务。

---

## 4. 技术亮点与优化点

### 结构化决策 (Structured Output)
QA 节点采用了 `with_structured_output(QAResult)`。这强制模型输出一个包含 `is_approved` (布尔值) 和 `feedback` (字符串) 的对象。

### 自动持久化 (Auto-Persistence)
新增的 `writer_node` 实现了从内存到磁盘的自动化：
*   **代码清理**: 自动剥离 Markdown 标签，确保保存的是可执行的源代码。
*   **物理路径管理**: 自动递归创建不存在的子目录。

### 健壮性与安全机制
*   **异常回退**: 在 QA 和 Writer 节点均有错误捕获逻辑，防止因 IO 权限或模型异常导致整个 Graph 崩溃。
*   **死循环防护**: 硬编码了 `iteration_count >= 3` 的触发条件，有效控制 Token 成本。

---

## 5. 如何运行

该脚本支持动态参数：
```python
# 示例：指定生成路径
initial_state = {
    "messages": [HumanMessage(content="帮我写一个数据处理脚本")],
    "file_path": "./src/utils/processor.py",
    "iteration_count": 0
}
```
