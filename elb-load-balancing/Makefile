export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION = us-east-1

usage:       ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

check:    ## Check if all required prerequisites are installed
	@command -v docker > /dev/null 2>&1 || { echo "Docker is not installed. Please install Docker and try again."; exit 1; }
	@command -v node > /dev/null 2>&1 || { echo "Node.js is not installed. Please install Node.js and try again."; exit 1; }
	@command -v lstk > /dev/null 2>&1 || { echo "lstk CLI is not installed. Please run: npm install -g @localstack/lstk"; exit 1; }
	@command -v aws > /dev/null 2>&1 || { echo "AWS CLI is not installed (required by 'lstk aws'). Please install it and try again."; exit 1; }
	@echo "All required prerequisites are available."


install:     ## Install dependencies
	@npm install
	@which serverless || npm install -g serverless
	@which lstk || npm install -g @localstack/lstk

run:         ## Deploy the app locally and run a Lambda test invocation
	echo "Deploying Serverless app to local environment"; \
	lstk aws s3api create-bucket --bucket testbucket; \
	SLS_DEBUG=1 npm run deploy && \
	echo "Serverless app successfully deployed. Now trying to invoke the Lambda functions via ELB endpoint." && \
	echo && echo "Invoking endpoint 1: http://lb-test-1.elb.localhost.localstack.cloud:4566/hello1" && \
	curl http://lb-test-1.elb.localhost.localstack.cloud:4566/hello1 && \
	echo && echo && echo "Invoking endpoint 2: http://lb-test-1.elb.localhost.localstack.cloud:4566/hello2" && \
	curl http://lb-test-1.elb.localhost.localstack.cloud:4566/hello2


start:
	@test -n "${LOCALSTACK_AUTH_TOKEN}" || (echo "LOCALSTACK_AUTH_TOKEN is not set. Find your token at https://app.localstack.cloud/workspace/auth-token"; exit 1)
	LOCALSTACK_DEBUG=1 LOCALSTACK_AUTH_TOKEN=$(LOCALSTACK_AUTH_TOKEN) lstk start --non-interactive --type aws

stop:
	@echo
	lstk stop
ready:
	@echo Waiting on the LocalStack container...
	@lstk status > /dev/null && echo Localstack is ready to use! || (echo Gave up waiting on LocalStack, exiting. && exit 1)

logs:
	@lstk logs > logs.txt

test-ci:
	make install start ready run; return_code=`echo $$?`;\
	make logs; make stop; exit $$return_code;

.PHONY: usage install start run stop ready logs test-ci
