"""Global model instance initialization."""

import os

from agent.model_config import get_model

# Configuration / 配置
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gemini")
model = get_model(DEFAULT_MODEL)
