export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION ?= us-east-1
SHELL := /bin/bash

usage:       ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

check:       ## Check if all required prerequisites are installed
	@command -v docker > /dev/null 2>&1 || { echo "Docker is not installed. Please install Docker and try again."; exit 1; }
	@command -v lstk > /dev/null 2>&1 || { echo "lstk CLI is not installed. Please run: npm install -g @localstack/lstk"; exit 1; }
	@command -v aws > /dev/null 2>&1 || { echo "AWS CLI is not installed (required by 'lstk aws'). Please install it and try again."; exit 1; }
	@echo "All required prerequisites are available."

install:     ## Install dependencies for the JavaScript sample
	@cd javascript && npm install

start:       ## Start LocalStack
	@test -n "${LOCALSTACK_AUTH_TOKEN}" || (echo "LOCALSTACK_AUTH_TOKEN is not set. Find your token at https://app.localstack.cloud/workspace/auth-token"; exit 1)
	lstk start --non-interactive --type aws
stop:        ## Stop LocalStack
	@echo
	lstk stop

ready:       ## Wait until LocalStack is ready
	@echo Waiting on the LocalStack container...
	@lstk status > /dev/null && echo LocalStack is ready to use! || (echo Gave up waiting on LocalStack, exiting. && exit 1)

logs:        ## Retrieve LocalStack logs
	@lstk logs > logs.txt

deploy:      ## Deploy the JavaScript Lambda with hot reloading enabled
	@cd javascript && \
		lstk aws iam create-role \
			--role-name lambda-role \
			--assume-role-policy-document file://trust-policy.json 2>/dev/null || true && \
		lstk aws lambda create-function \
			--function-name hot-reload-js \
			--runtime nodejs18.x \
			--role arn:aws:iam::000000000000:role/lambda-role \
			--code S3Bucket=hot-reload,S3Key=$$(pwd) \
			--handler index.handler

wait:        ## Wait until the Lambda function can be invoked
	@lstk aws lambda wait function-active-v2 --function-name hot-reload-js

run:         ## Invoke the hot-reload Lambda function
	@lstk aws lambda invoke \
		--function-name hot-reload-js \
		--payload '{}' \
		output.json && cat output.json

test-ci:     ## Run CI tests
	make check start install ready deploy wait run; return_code=`echo $$?`;\
	make logs; make stop; exit $$return_code;

.PHONY: usage check install start stop ready logs deploy wait run test-ci
