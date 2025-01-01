# Default port for the application (can be overridden)
PORT ?= 7601

.PHONY: test docker-build docker-run install-hooks setup help

help:
	@echo "Available targets:"
	@echo "  make test              Run tests with coverage"
	@echo "  make docker-build      Build Docker image"
	@echo "  make docker-run        Run Docker container (default port: 8000)"
	@echo "  make install-hooks     Install git hooks"
	@echo "  make setup            Install project and git hooks"
	@echo ""
	@echo "To run on a different port:"
	@echo "  make docker-run PORT=<port>"
	@echo "Example:"
	@echo "  make docker-run PORT=3000"

test:
	pytest \
		--cov=app \
		--cov-report=term-missing \
		--cov-report=html \
		--cov-fail-under=90 \
		-v \
		tests/

docker-build:
	docker build -t secrets-api .

docker-run:
	docker run -p $(PORT):8000 secrets-api

install-hooks:
	git config core.hooksPath .githooks

setup: install-hooks
	pip install -e .
