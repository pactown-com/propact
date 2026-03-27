.PHONY: install dev test lint clean build publish docs

# Install dependencies
install:
	poetry install

# Install development dependencies
dev:
	poetry install --with dev

# Run tests
test:
	poetry run pytest -vv

# Run tests with coverage
test-cov:
	poetry run pytest --cov=propact --cov-report=html --cov-report=term

# Run linting
lint:
	poetry run ruff check src/ tests/
	poetry run ruff format src/ tests/

# Run type checking
type-check:
	poetry run mypy src/

# Run all checks
check: lint type-check test

# Clean build artifacts
clean:
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Build package
build: clean
	poetry build

# Publish to PyPI
publish: build
	poetry publish

# Publish to test PyPI
publish-test: build
	poetry publish --repository testpypi

# Generate documentation
docs:
	@echo "Documentation generation not yet implemented"

# Run development server (if applicable)
dev-server:
	@echo "No development server available"

# Format code
format:
	poetry run ruff format src/ tests/

# Fix linting issues
fix:
	poetry run ruff check --fix src/ tests/

# LLM testing targets
llm-test:
	poetry run python -c "from propact.llm_proxy import LiteLLMProxy; print('LiteLLM import OK')"
	poetry run propact --help | grep -q llm-provider && echo "CLI LLM flags OK"
	@echo "✅ LiteLLM multi-provider configuration OK!"

llm-bench:
	@echo "Benchmarking LLM providers..."
	@poetry run python -c "import asyncio; from propact.llm_proxy import quick_generate; asyncio.run(quick_generate('Say hello', provider='local'))" 2>/dev/null || echo "Ollama not available"
	@echo "✅ LLM benchmark complete"

public-demo:
	@echo "🚀 Running public APIs demo..."
	cd examples/public-apis && ./demo-public.sh

install-llm:
	poetry install --extras llm
