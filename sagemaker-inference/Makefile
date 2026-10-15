export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION ?= us-east-1
SHELL := /bin/bash

usage:       ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

check:       ## Check if all required prerequisites are installed
	@command -v docker > /dev/null 2>&1 || { echo "Docker is not installed. Please install Docker and try again."; exit 1; }
	@command -v python3 > /dev/null 2>&1 || { echo "Python 3 is not installed. Please install Python 3 and try again."; exit 1; }
	@command -v lstk > /dev/null 2>&1 || { echo "lstk CLI is not installed. Please run: npm install -g @localstack/lstk"; exit 1; }
	@echo "All required prerequisites are available."

install:     ## Install Python dependencies
	@pip install -r requirements.txt

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

run:         ## Run the SageMaker inference example
	@python3 main.py

test-ci:     ## Run CI tests
	make check start install ready run; return_code=`echo $$?`;\
	make logs; make stop; exit $$return_code;

.PHONY: usage check install start stop ready logs run test-ci
