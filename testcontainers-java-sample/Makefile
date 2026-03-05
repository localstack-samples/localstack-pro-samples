export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION ?= us-east-1
SHELL := /bin/bash

usage:       ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

check:       ## Check if all required prerequisites are installed
	@command -v docker > /dev/null 2>&1 || { echo "Docker is not installed. Please install Docker and try again."; exit 1; }
	@command -v mvn > /dev/null 2>&1 || { echo "Maven is not installed. Please install Maven and try again."; exit 1; }
	@command -v java > /dev/null 2>&1 || { echo "Java is not installed. Please install Java and try again."; exit 1; }
	@echo "All required prerequisites are available."

install:     ## Compile the Java application
	@cd LocalStackTestcontainers && mvn compile -q

start:       ## Check LocalStack auth token (Testcontainers manages the container lifecycle)
	@test -n "${LOCALSTACK_AUTH_TOKEN}" || (echo "LOCALSTACK_AUTH_TOKEN is not set. Find your token at https://app.localstack.cloud/workspace/auth-token"; exit 1)
	@echo "LocalStack auth token is set. Testcontainers will manage the LocalStack container lifecycle."

stop:        ## No-op: Testcontainers manages container lifecycle
	@echo "Testcontainers manages the LocalStack container lifecycle."

ready:       ## No-op: Testcontainers manages container lifecycle
	@echo "Testcontainers manages the LocalStack container lifecycle."

logs:        ## Retrieve LocalStack logs from Maven test output
	@echo "Check Maven Surefire test reports in LocalStackTestcontainers/target/surefire-reports/"

run:         ## Run the Testcontainers integration tests
	@cd LocalStackTestcontainers && LOCALSTACK_AUTH_TOKEN=${LOCALSTACK_AUTH_TOKEN} mvn test

test-ci:     ## Run CI tests
	make check install run; return_code=`echo $$?`;\
	make logs; exit $$return_code;

.PHONY: usage check install start stop ready logs run test-ci
