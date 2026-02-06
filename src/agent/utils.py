"""Utility functions for the software factory agent."""

import os
from typing import List

from langchain_core.messages import AnyMessage


def get_last_message_content(messages: List[AnyMessage]) -> str:
    """Safely extract content from the last message in the history. / 安全地从历史记录中的最后一条消息中提取内容。."""
    if not messages:
        return ""
    last_msg = messages[-1]
    if isinstance(last_msg, dict):
        return last_msg.get("content", "")
    return getattr(last_msg, "content", str(last_msg))

def get_project_structure(root_dir: str = ".", exclude_dirs: List[str] | None = None) -> str:
    """Scan the directory to create a text-based tree structure. / 扫描目录以创建基于文本的 tree 结构。."""
    if exclude_dirs is None:
        env_excludes = os.getenv("PROJECT_EXCLUDES", "")
        if env_excludes:
            exclude_dirs = [d.strip() for d in env_excludes.split(",")]
        else:
            exclude_dirs = [".git", "__pycache__", ".venv", "node_modules", ".agent", "agent.egg-info", "static", ".langgraph_api"]
    
    root_dir = os.path.abspath(root_dir)
    tree = [f"Project Root: {root_dir}"]
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        level = root.replace(root_dir, '').count(os.sep)
        indent = '  ' * level
        tree.append(f"{indent}{os.path.basename(root) or root}/")
        sub_indent = '  ' * (level + 1)
        for f in files:
            if not f.startswith('.'):
                tree.append(f"{sub_indent}{f}")
    
    return "\n".join(tree)

def read_project_guidelines(root_dir: str) -> str:
    """Find and read key documentation/guideline files, including AI-specific rules and skills. / 查找并读取关键文档/规范文件，包括 AI 特定的规则和技能文档。."""
    root_dir = os.path.abspath(root_dir)
    context = []
    
    standard_files = [
        "README.md", 
        "CONTRIBUTING.md", 
        "DEVELOPMENT.md"
    ]
    
    to_process = []
    try:
        items = os.listdir(root_dir)
        for item in items:
            item_path = os.path.join(root_dir, item)
            item_lower = item.lower()
            if item in standard_files:
                to_process.append(item_path)
            elif item_lower.startswith("ai"):
                to_process.append(item_path)
            elif item == ".agent":
                to_process.append(item_path)
    except Exception as e:
        return f"Error scanning project root: {str(e)}"

    def read_md_files_recursively(path):
        if os.path.isfile(path):
            if path.lower().endswith(".md"):
                try:
                    with open(path, encoding="utf-8") as f:
                        rel_path = os.path.relpath(path, root_dir)
                        content = f.read()
                        context.append(f"--- CONTENT OF {rel_path} ---\n{content}")
                except Exception as e:
                    context.append(f"Error reading {path}: {str(e)}")
        elif os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                if any(x in root for x in [".git", "node_modules", "venv", "__pycache__"]):
                    continue
                for f in files:
                    if f.lower().endswith(".md"):
                        file_full_path = os.path.join(root, f)
                        read_md_files_recursively(file_full_path)

    for path in to_process:
        read_md_files_recursively(path)
                    
    return "\n\n".join(context) if context else "No project-specific guidelines found. / 未发现特定于项目的指导规范。"

def save_file_sync(file_path: str, clean_code: str):
    """Write the generated code to the local filesystem. / 将生成的代码保存到本地文件系统。."""
    abs_path = os.path.abspath(file_path)
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    with open(abs_path, "w", encoding="utf-8") as f:
        f.write(clean_code)
