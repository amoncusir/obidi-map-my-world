SOURCE_DIR = src
TEST_DIR = tests
PROJECT_DIRS = $(SOURCE_DIR) $(TEST_DIR)
PWD := $(dir $(abspath $(firstword $(MAKEFILE_LIST))))
PROJECT_VERSION ?= v$(shell poetry version -s)
PROJECT_NAME ?= mapmyworld
PYTHON_VERSION ?= $(shell cat .python-version)

.PHONY: build
build:
	docker build -t "${PROJECT_NAME}:latest" -t "${PROJECT_NAME}:${PROJECT_VERSION}" -f "${PWD}infrastructure/Dockerfile" ${PWD}

clean:
	find "${PWD}src/" -name "__pycache__" -type d -exec rm -rfv {} +

test:
	poetry run pytest --cov=$(SOURCE_DIR) -s --capture=no --log-cli-level=0 $(TEST_DIR)

ci-test:
	# No runs the integration tests due an existent TestContainer bug in v4.X with Docker-in-Docker environments
	# Issue: https://github.com/testcontainers/testcontainers-python/issues/475
	poetry run pytest --cov-report xml:report/coverage.xml --cov=$(SOURCE_DIR) --junit-xml=report/test.xml "$(TEST_DIR)/unittests/"

.PHONY: pre-commit lint
lint: pre-commit
pre-commit:
	pre-commit run --all-files

.PHONY: info
info:
	@echo "${PROJECT_NAME};${PROJECT_VERSION};${PYTHON_VERSION}"

.PHONY: run-services
run-services:
	docker compose up -d


.PHONY: run-api
run-api:
	fastapi dev --app api 'src/app/api_instance.py'
