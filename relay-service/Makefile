.PHONY: lint check test run-locally run-docker stop-docker

export PYTHONPATH := $(shell pwd)/src
export ENV_FILE := .env

lint:
	ruff format .
	ruff check . --fix

check:
	mypy . --config-file=mypy.ini

test:
	ENVIRONMENT=test pytest -v

run-locally:
	@echo "Running FastAPI app locally with .env loaded..."
	. $(ENV_FILE) && ENVIRONMENT=local uvicorn relay_service.app:app --reload --port 8000

run-docker:
	@echo "Running docker compose with .env loaded..."
	docker compose up -d --build

stop-docker:
	@echo "Stopping docker & killing volume"
	docker compose down -v