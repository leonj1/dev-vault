# Default ports for the application (can be overridden)
API_PORT ?= 7601
FRONTEND_PORT ?= 7600
API_CONTAINER := secrets-api
FRONTEND_CONTAINER := secrets-frontend

.PHONY: test install-hooks setup help run stop build build-frontend

help:
	@echo "Available targets:"
	@echo "  make test              Run tests with coverage"
	@echo "  make install-hooks     Install git hooks"
	@echo "  make setup             Install project and git hooks"
	@echo "  make build             Build API Docker image"
	@echo "  make build-frontend    Build frontend Docker image"
	@echo "  make run               Run the application"
	@echo "  make stop              Stop the application"
	@echo ""
	@echo "To run on different ports:"
	@echo "  make run API_PORT=<port> FRONTEND_PORT=<port>"
	@echo "Example:"
	@echo "  make run API_PORT=7601 FRONTEND_PORT=3000"
	@echo ""
	@echo "Default ports:"
	@echo "  API: $(API_PORT)"
	@echo "  Frontend: $(FRONTEND_PORT)"

test:
	pytest \
		--cov=app \
		--cov-report=term-missing \
		--cov-report=html \
		--cov-fail-under=70 \
		-v \
		tests/

build: build-frontend
	docker build -t $(API_CONTAINER) .

build-frontend:
	docker build -t $(FRONTEND_CONTAINER) -f Dockerfile.frontend .

run: stop build build-frontend
	@echo "Starting API server and frontend..."
	@docker run -d --name $(API_CONTAINER) -p $(API_PORT):8000 $(API_CONTAINER)
	@sleep 2  # Wait for API to start
	@docker run -d --name $(FRONTEND_CONTAINER) \
		-e API_HOST=10.1.1.144 \
		-e API_PORT=$(API_PORT) \
		-p $(FRONTEND_PORT):3000 \
		$(FRONTEND_CONTAINER)

stop:
	@echo "Stopping containers..."
	-@docker stop -t 0 $(API_CONTAINER) $(FRONTEND_CONTAINER) || true
	-@docker rm -f $(API_CONTAINER) $(FRONTEND_CONTAINER) || true
	@sleep 1  # Wait for processes to clean up

install-hooks:
	git config core.hooksPath .githooks

setup: install-hooks
	pip install -e .
