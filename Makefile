.PHONY: dev test format lint
dev:
	uv run uvicorn app.main:app --reload
test:
	uv run pytest
format:
	uv run black app tests
lint:
	uv run ruff check app tests
