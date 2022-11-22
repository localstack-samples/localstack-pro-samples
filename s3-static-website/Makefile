export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION = us-east-1
SHELL := /bin/bash
PYTHON_BIN ?= $(shell which python3 || which python)

usage:      ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:    ## Install dependencies
	@which localstack || pip install localstack
	@which awslocal || pip install awscli-local
	@test -e .venv || ($(PYTHON_BIN) -m venv .venv; source .venv/bin/activate; pip install wheel; pip install psycopg2-binary boto3)

run:        
	awslocal s3api create-bucket --bucket testwebsite
	awslocal s3api put-bucket-policy --bucket testwebsite --policy file://bucket_policy.json
	awslocal s3 sync ./ s3://testwebsite
	awslocal s3 website s3://testwebsite/ --index-document www/index.html --error-document www/error.html

start:
	localstack start -d

stop:
	@echo
	localstack stop
ready:
	@echo Waiting on the LocalStack container...
	@localstack wait -t 30 && echo Localstack is ready to use! || (echo Gave up waiting on LocalStack, exiting. && exit 1)

logs:
	@localstack logs > logs.txt

test-ci:
	make start install ready run; return_code=`echo $$?`;\
	make logs; make stop; exit $$return_code;
	
.PHONY: usage install start run stop ready logs test-ci
