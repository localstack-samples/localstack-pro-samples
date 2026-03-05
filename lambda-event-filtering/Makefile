export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION ?= us-east-1
SHELL := /bin/bash

usage:       ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

check:       ## Check if all required prerequisites are installed
	@command -v docker > /dev/null 2>&1 || { echo "Docker is not installed. Please install Docker and try again."; exit 1; }
	@command -v node > /dev/null 2>&1 || { echo "Node.js is not installed. Please install Node.js and try again."; exit 1; }
	@command -v localstack > /dev/null 2>&1 || { echo "LocalStack CLI is not installed. Please install it and try again."; exit 1; }
	@command -v samlocal > /dev/null 2>&1 || { echo "samlocal is not installed. Please run: pip install aws-sam-cli-local"; exit 1; }
	@command -v awslocal > /dev/null 2>&1 || { echo "awslocal is not installed. Please run: pip install awscli-local"; exit 1; }
	@echo "All required prerequisites are available."

install:     ## Install dependencies
	@npm install

start:       ## Start LocalStack
	@test -n "${LOCALSTACK_AUTH_TOKEN}" || (echo "LOCALSTACK_AUTH_TOKEN is not set. Find your token at https://app.localstack.cloud/workspace/auth-token"; exit 1)
	localstack start -d

stop:        ## Stop LocalStack
	@echo
	localstack stop

ready:       ## Wait until LocalStack is ready
	@echo Waiting on the LocalStack container...
	@localstack wait -t 30 && echo LocalStack is ready to use! || (echo Gave up waiting on LocalStack, exiting. && exit 1)

logs:        ## Retrieve LocalStack logs
	@localstack logs > logs.txt

deploy:      ## Deploy the SAM application to LocalStack
	@samlocal build
	@samlocal deploy --no-confirm-changeset --resolve-s3 --stack-name lambda-event-filtering

run:         ## Send a test SQS message to trigger the Lambda function
	@awslocal sqs send-message \
		--queue-url http://localhost:4566/000000000000/MyQueue \
		--message-body '{"data": "A"}' \
		--delay-seconds 10

test-ci:     ## Run CI tests
	make check start install ready deploy run; return_code=`echo $$?`;\
	make logs; make stop; exit $$return_code;

.PHONY: usage check install start stop ready logs deploy run test-ci
