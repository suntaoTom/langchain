"""Model configuration management for the agent.

This module provides a factory to get specific models based on configuration.
Supports:
- Gemini (via ChatGoogleGenerativeAI)
- Alibaba Qwen (via ChatOpenAI compatible endpoint or DashScope)
- DeepSeek (via ChatOpenAI compatible endpoint)
"""

import os
from typing import Literal

from dotenv import load_dotenv
from langchain_core.language_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

# Load environment variables early
load_dotenv()

# Define supported model types
ModelProvider = Literal["gemini", "qwen", "deepseek", "ollama"]

def get_model(provider: ModelProvider = "gemini", temperature: float = 0) -> BaseChatModel:
    """Get a chat model instance based on the provider."""
    if provider == "gemini":
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables.")
        return ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            temperature=temperature,
            google_api_key=api_key
        )
        
    elif provider == "qwen":
        # Alibaba Qwen (DashScope)
        # Often compatible with OpenAI client if base_url is set, 
        # or use langchain_community.chat_models.ChatTongyi for native support.
        # Here we assume OpenAI compatibility for simplicity, or we can use ChatTongyi if preferred.
        # User requested "Ali Qwen", let's try the standard OpenAI-compatible route first 
        # as it's cleaner, but DashScope has a specific URL.
        api_key = os.getenv("DASHSCOPE_API_KEY")
        if not api_key:
            raise ValueError("DASHSCOPE_API_KEY not found. Please set it for Alibaba Qwen.")
            
        return ChatOpenAI(
            model="qwen-turbo", # or qwen-max
            temperature=temperature,
            api_key=api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
        
    elif provider == "deepseek":
        # DeepSeek API
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY not found. Please set it for DeepSeek.")
            
        return ChatOpenAI(
            model="deepseek-chat", 
            temperature=temperature,
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )
        
    elif provider == "ollama":
        # Local Ollama
        model_name = os.getenv("OLLAMA_MODEL", "llama3")
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        
        return ChatOllama(
            model=model_name,
            temperature=temperature,
            base_url=base_url
        )
        
    else:
        raise ValueError(f"Unsupported provider: {provider}")

# Removed top-level initialization to prevent errors if keys are missing.
# Use get_model() at runtime instead.
