"""Manual test for model configuration."""

import logging
import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

from agent.model_config import get_model

load_dotenv()
logger = logging.getLogger(__name__)

def test_model():
    """Test the model configuration and connectivity."""
    provider = os.getenv("DEFAULT_MODEL", "gemini")
    logger.info("Testing provider: %s", provider)
    try:
        model = get_model(provider)
        response = model.invoke([HumanMessage(content="Hello, who are you?")])
        logger.info("Response received:")
        logger.info(response.content)
    except Exception:
        logger.exception("Error in test_model")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_model()
