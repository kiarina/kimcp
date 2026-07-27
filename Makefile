.PHONY: init update upgrade format lint test clean build publish
.DEFAULT_GOAL := build

init:
	mise run setup

update:
	uv sync --all-extras --all-groups

upgrade:
	mise run upgrade --sync

format:
	uv run ruff format kimcp/ tests/

lint:
	uv run ruff check kimcp/ tests/
	uv run ruff format --check kimcp/ tests/
	uv run mypy kimcp/

test:
	uv run pytest --cov=kimcp tests/

clean:
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +

build: format lint test clean
	uv build

publish: build
	uv publish
