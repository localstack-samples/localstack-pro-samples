export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION ?= us-east-1
SHELL := /bin/bash

S3_BUCKET ?= test-emr-bucket
JOB_ROLE_ARN ?= arn:aws:iam::000000000000:role/emr-serverless-job-role

usage:       ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

check:       ## Check if all required prerequisites are installed
	@command -v docker > /dev/null 2>&1 || { echo "Docker is not installed. Please install Docker and try again."; exit 1; }
	@command -v localstack > /dev/null 2>&1 || { echo "LocalStack CLI is not installed. Please install it and try again."; exit 1; }
	@command -v awslocal > /dev/null 2>&1 || { echo "awslocal is not installed. Please run: pip install awscli-local"; exit 1; }
	@command -v mvn > /dev/null 2>&1 || { echo "Maven is not installed. Please install Maven and try again."; exit 1; }
	@echo "All required prerequisites are available."

install:     ## Build the Java application
	@cd hello-world && mvn package -q

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

deploy:      ## Create S3 bucket and upload the JAR file
	@awslocal s3 mb s3://$(S3_BUCKET) || true
	@awslocal s3 cp hello-world/target/hello-world-1.0.jar s3://$(S3_BUCKET)/code/hello-world-1.0.jar

run:         ## Create and run an EMR Serverless job
	$(eval APP_ID := $(shell awslocal emr-serverless create-application \
		--type SPARK \
		--name hello-world-demo \
		--release-label emr-6.9.0 \
		--query applicationId --output text))
	@echo "Application ID: $(APP_ID)"
	@awslocal emr-serverless start-application --application-id $(APP_ID)
	@awslocal emr-serverless start-job-run \
		--application-id $(APP_ID) \
		--execution-role-arn $(JOB_ROLE_ARN) \
		--job-driver '{"sparkSubmit": {"entryPoint": "s3://$(S3_BUCKET)/code/hello-world-1.0.jar"}}'

test-ci:     ## Run CI tests
	make check start install ready deploy run; return_code=`echo $$?`;\
	make logs; make stop; exit $$return_code;

.PHONY: usage check install start stop ready logs deploy run test-ci
