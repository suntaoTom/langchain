import os
from dotenv import load_dotenv
from agent.model_config import get_model
from langchain_core.messages import HumanMessage

load_dotenv()

def test_model():
    provider = os.getenv("DEFAULT_MODEL", "gemini")
    print(f"Testing provider: {provider}")
    try:
        model = get_model(provider)
        response = model.invoke([HumanMessage(content="Hello, who are you?")])
        print("Response received:")
        print(response.content)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_model()
