uv sync或者pip install

pkill -f "langgraph dev"

uv run langgraph dev

# 强制清理端口并带着“禁用代理”标志启动
kill $(lsof -t -i:2024) 2>/dev/null

NO_PROXY=127.0.0.1,localhost uv run langgraph dev