# Makefile for DFM OSINT Backend

# Variables
PYTHON := python
PIP := pip
UVICORN := uvicorn
APP := main:app
HOST := 0.0.0.0
PORT := 8000

# Default target
.PHONY: help
help:
	@echo "DFM OSINT Backend Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  install     Install dependencies"
	@echo "  dev         Start development server"
	@echo "  test        Run tests"
	@echo "  clean       Clean temporary files"
	@echo "  help        Show this help message"

# Install dependencies
.PHONY: install
install:
	$(PIP) install -r requirements.txt

# Start development server
.PHONY: dev
dev:
	$(UVICORN) $(APP) --host $(HOST) --port $(PORT) --reload

# Run tests
.PHONY: test
test:
	$(PYTHON) -m pytest tests/ -v

# Clean temporary files
.PHONY: clean
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

# Install development dependencies
.PHONY: install-dev
install-dev:
	$(PIP) install -r requirements.txt
	$(PIP) install pytest black flake8

# Format code
.PHONY: format
format:
	black .
	flake8 .

# Run linting
.PHONY: lint
lint:
	flake8 .