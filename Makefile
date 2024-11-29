SHELL := /bin/bash

.PHONY: init
init: setup-lambda-runtime-init
	@python -c 'import sys; assert sys.version_info >= (3, 10) and sys.version_info < (3, 12), "Python version must be 3.10 or 3.11"'
	@echo "Initializing virtual environment in .venv"
	@if [ ! -d ".venv" ]; then python -m venv .venv; fi
	@echo "Installing dependencies"
	@source .venv/bin/activate; pip install -qr requirements-dev.txt
	@echo "Installing pre-commit"
	@source .venv/bin/activate; pre-commit install
	@echo "Please run 'source .venv/bin/activate' to activate the virtual environment"

.PHONY: format
format:
	@ruff format src/ tests/

.PHONY: ruff
ruff:
	@ruff check src/ tests/

.PHONY: isort
isort:
	@isort src/ tests/

.PHONY: mypy
mypy:
	@mypy src/ tests/

.PHONY: fixit
fixit:
	fixit lint src/ tests/

.PHONY: test
test:
	ENV=test pytest --cov-fail-under=95 --cov=src/ --cov-report=term-missing --cov-report=xml

.PHONY: shell
shell:
	ENV=local python

.PHONY: compile-regular-dependencies
compile-regular-dependencies:
	@pip-compile --allow-unsafe --no-emit-index-url requirements.in

.PHONY: compile-dev-dependencies
compile-dev-dependencies:
	@pip-compile --allow-unsafe --no-emit-index-url requirements-dev.in


.PHONY: lint
lint: format ruff mypy isort fixit

.PHONY: compile-dependencies
compile-dependencies: compile-regular-dependencies compile-dev-dependencies

.PHONY: setup-lambda-runtime-init
setup-lambda-runtime-init:
	scripts/install-lambda-runtime-init.sh
