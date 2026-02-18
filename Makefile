SHELL := /bin/zsh

.PHONY: help setup run langchain langgraph check clean

help:
	@echo "Targets:"
	@echo "  make setup      Create venv and install dependencies with uv"
	@echo "  make run        Run both demos (main.py)"
	@echo "  make langchain  Run only LangChain demo"
	@echo "  make langgraph  Run only LangGraph demo"
	@echo "  make check      Parse-check Python files"
	@echo "  make clean      Remove virtual environment and caches"

setup:
	uv venv
	uv sync
	@if [ ! -f .env ]; then cp .env.example .env; echo "Created .env from .env.example"; fi

run:
	uv run python main.py

langchain:
	uv run python -m demo.langchain_demo

langgraph:
	uv run python -m demo.langgraph_demo

check:
	uv run python -c "import ast, pathlib; files=[pathlib.Path('main.py')] + list(pathlib.Path('src').rglob('*.py')); [ast.parse(f.read_text(), filename=str(f)) for f in files]; print(f'Parsed {len(files)} Python files successfully')"

clean:
	rm -rf .venv .pytest_cache __pycache__ src/**/__pycache__
