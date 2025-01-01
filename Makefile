# Default port for the application (can be overridden)
PORT ?= 7601
CONTAINER_NAME := secrets-api

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

build:
	docker build -t $(CONTAINER_NAME) .

run:
	docker run -d --rm --name $(CONTAINER_NAME) -p $(PORT):8000 $(CONTAINER_NAME)

stop:
	docker stop -t 0 $(CONTAINER_NAME) || true
	docker rm -f $(CONTAINER_NAME) || true

install-hooks:
	git config core.hooksPath .githooks

setup: install-hooks
	pip install -e .
