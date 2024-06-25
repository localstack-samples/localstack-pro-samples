# Enforce IAM to test cross-account cross-region access
export ENFORCE_IAM=1
export DEBUG=1

SHELL := /bin/bash

usage:       ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:     ## Install dependencies
	@which localstack || pip install localstack
	@which awslocal || pip install awscli-local

run:         ## Run the cross-account cross-region experiment of copying data from one S3 bucket to another
	./run.sh

start:       ## Start LocalStack
	localstack start -d

stop:        ## Stop LocalStack
	@echo
	localstack stop

ready:       ## Wait for LocalStack to be ready
	@echo Waiting on the LocalStack container...
	@localstack wait -t 30 && echo Localstack is ready to use! || (echo Gave up waiting on LocalStack, exiting. && exit 1)

logs:        ## Retrieve logs from LocalStack
	@localstack logs > logs.txt

test-ci:     ## Run CI test
	make start install ready run; return_code=`echo $$?`;\
	make logs; make stop; exit $$return_code;

.PHONY: usage install start run stop ready logs test-ci
