.PHONY: help venv act deact install install-dev test test-cov lint format format-check clean

help:
	@echo "PDFTools Makefile - Available targets:"
	@echo ""
	@echo "  make venv              Create virtual environment (pdfenv)"
	@echo "  make act               Activate virtual environment (pdfenv)"
	@echo "  make deact             Deactivate virtual environment"
	@echo "  make install           Install project dependencies"
	@echo "  make install-dev       Install project with dev dependencies"
	@echo "  make test              Run tests with pytest"
	@echo "  make test-cov          Run tests with coverage report"
	@echo "  make lint              Check code style with flake8"
	@echo "  make format            Format code with black and isort"
	@echo "  make format-check      Check if code needs formatting"
	@echo "  make clean             Remove build artifacts and cache files"
	@echo "  make help              Show this help message"

venv:
	python3 -m venv pdfenv
	@echo "Virtual environment 'pdfenv' created. Activate it with: source pdfenv/bin/activate"

act:
	@bash -c "source pdfenv/bin/activate && bash"

deact:
	@echo "To deactivate the virtual environment, type: deactivate"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

test:
	pytest

test-cov:
	pytest --cov=pdftools --cov-report=html --cov-report=term-missing

lint:
	flake8 pdftools tests scripts

format:
	isort pdftools tests scripts
	black pdftools tests scripts

format-check:
	isort --check-only pdftools tests scripts
	black --check pdftools tests scripts

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete
	find . -type d -name '*.egg-info' -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ .pytest_cache/ .coverage htmlcov/
