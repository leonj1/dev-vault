.PHONY: test docker-build docker-run

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
	docker run -p 8000:8000 secrets-api
