export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION ?= us-east-1
SHELL := /bin/bash

usage:       ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

check:       ## Check if all required prerequisites are installed
	@command -v docker > /dev/null 2>&1 || { echo "Docker is not installed. Please install Docker and try again."; exit 1; }
	@command -v mvn > /dev/null 2>&1 || { echo "Maven is not installed. Please install Maven and try again."; exit 1; }
	@command -v lstk > /dev/null 2>&1 || { echo "lstk CLI is not installed (required by 'lstk aws'). Please run: npm install -g @localstack/lstk"; exit 1; }
	@command -v aws > /dev/null 2>&1 || { echo "AWS CLI is not installed (required by 'lstk aws'). Please install it and try again."; exit 1; }
	@echo "All required prerequisites are available."

install:     ## Build the Java application
	@mvn clean install -q

start:       ## Start LocalStack and supporting services via Docker Compose
	@test -n "${LOCALSTACK_AUTH_TOKEN}" || (echo "LOCALSTACK_AUTH_TOKEN is not set. Find your token at https://app.localstack.cloud/workspace/auth-token"; exit 1)
	LOCALSTACK_AUTH_TOKEN=${LOCALSTACK_AUTH_TOKEN} docker compose up -d

stop:        ## Stop all services
	@echo
	docker compose down

ready:       ## Wait until LocalStack is ready
	@echo Waiting on the LocalStack container...
	@for i in $$(seq 1 30); do curl -sf http://localhost:4566/_localstack/health > /dev/null && break; sleep 1; done; \
		curl -sf http://localhost:4566/_localstack/health > /dev/null && echo LocalStack is ready to use! || (echo Gave up waiting on LocalStack, exiting. && exit 1)

logs:        ## Retrieve LocalStack logs
	@docker compose logs localstack > logs.txt

deploy:      ## Deploy CloudFormation stack for notification infrastructure
	@lstk aws cloudformation deploy \
		--template-file src/main/resources/email-infra.yml \
		--stack-name email-infra

run:         ## Start the Spring Boot application and run a test notification
	@lstk aws ses verify-email-identity --email-address no-reply@localstack.cloud
	AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test mvn spring-boot:run &
	@sleep 5
	@lstk aws sns publish \
		--topic arn:aws:sns:us-east-1:000000000000:email-notifications \
		--message '{"subject":"hello", "address": "alice@example.com", "body": "hello world"}'
	@curl -s localhost:8080/process

test-ci:     ## Run CI tests
	make check start install ready deploy run; return_code=`echo $$?`;\
	make logs; make stop; exit $$return_code;

.PHONY: usage check install start stop ready logs deploy run test-ci
