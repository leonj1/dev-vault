.PHONY: test

test:
	pytest \
		--cov=app \
		--cov-report=term-missing \
		--cov-report=html \
		--cov-fail-under=90 \
		-v \
		tests/
