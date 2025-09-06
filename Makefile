.PHONY: dev lint test fmt install

# Development server
dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Install dependencies
install:
	pip install -e ".[dev]"

# Linting
lint:
	ruff check .
	black --check .
	isort --check-only .

# Format code
fmt:
	black .
	isort .
	ruff check --fix .

# Run tests
test:
	pytest -v

# Run tests with coverage
test-cov:
	pytest --cov=app --cov-report=html --cov-report=term

# Clean up
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
