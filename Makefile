.PHONY: test build run

CONTAINER_NAME := secrets-api
PORT=7601

test:
	pytest \
		--cov=app \
		--cov-report=term-missing \
		--cov-report=html \
		--cov-fail-under=90 \
		-v \
		tests/

build:
	docker build -t secrets-api .

run:
	docker run -p $(PORT):8000 $(CONTAINER_NAME)

stop:
	docker stop -t 0 $(CONTAINER_NAME) || true
	docker rm -f $(CONTAINER_NAME) || true

