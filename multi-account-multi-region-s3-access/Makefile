# Enforce IAM to test cross-account cross-region access
export LOCALSTACK_ENFORCE_IAM=1
export DEBUG=1

SHELL := /bin/bash

usage:       ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

check:    ## Check if all required prerequisites are installed
	@command -v docker > /dev/null 2>&1 || { echo "Docker is not installed. Please install Docker and try again."; exit 1; }
	@command -v lstk > /dev/null 2>&1 || { echo "lstk CLI is not installed. Please run: npm install -g @localstack/lstk"; exit 1; }
	@command -v awslocal > /dev/null 2>&1 || { echo "awslocal is not installed. Please run: pip install awscli-local"; exit 1; }
	@echo "All required prerequisites are available."


install:     ## Install dependencies
	@which lstk > /dev/null || npm install -g @localstack/lstk
	@which awslocal || pip install awscli-local

run:         ## Run the cross-account cross-region experiment of copying data from one S3 bucket to another
	./run.sh

start:       ## Start LocalStack
	@test -n "${LOCALSTACK_AUTH_TOKEN}" || (echo "LOCALSTACK_AUTH_TOKEN is not set. Find your token at https://app.localstack.cloud/workspace/auth-token"; exit 1)
	lstk start --non-interactive --type aws
stop:        ## Stop LocalStack
	@echo
	lstk stop

ready:       ## Wait for LocalStack to be ready
	@echo Waiting on the LocalStack container...
	@lstk status > /dev/null && echo Localstack is ready to use! || (echo Gave up waiting on LocalStack, exiting. && exit 1)

logs:        ## Retrieve logs from LocalStack
	@lstk logs > logs.txt

test-ci:     ## Run CI test
	make start install ready run; return_code=`echo $$?`;\
	make logs; make stop; exit $$return_code;

.PHONY: usage install start run stop ready logs test-ci
