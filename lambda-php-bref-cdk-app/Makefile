export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION ?= us-east-1

# Using composer Docker image to avoid local PHP dependency:
# https://hub.docker.com/_/composer
DOCKER_COMPOSER_IMAGE ?= composer:2.5

usage:       ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

check:    ## Check if all required prerequisites are installed
	@command -v docker > /dev/null 2>&1 || { echo "Docker is not installed. Please install Docker and try again."; exit 1; }
	@command -v node > /dev/null 2>&1 || { echo "Node.js is not installed. Please install Node.js and try again."; exit 1; }
	@command -v localstack > /dev/null 2>&1 || { echo "LocalStack CLI is not installed. Please install it and try again."; exit 1; }
	@command -v awslocal > /dev/null 2>&1 || { echo "awslocal is not installed. Please run: pip install awscli-local"; exit 1; }
	@echo "All required prerequisites are available."


install:     ## Install dependencies
	@npm install
	@which cdklocal || npm install -g aws-cdk-local aws-cdk
	@which localstack || pip install localstack
	echo "Install Bref PHP dependencies via composer"
	make install-bref-docker

install-bref:
	cd backend && \
	composer install

install-bref-docker:	## Install Bref dependencies via composer into backend/vendor
	cd backend && \
	docker run --rm --volume $$PWD:/app --user $$(id -u):$$(id -g) $(DOCKER_COMPOSER_IMAGE) composer install

run:         ## Deploy the app locally and invoke Lambda through API gateway
	echo "Bootstrapping CDK"; \
	cdklocal bootstrap && \
	echo "Deploying CDK app to local environment"; \
	cdklocal deploy --outputs-file cdk-outputs.json --require-approval never && \
	echo "CDK app successfully deployed. Now trying to invoke the Lambda through API gateway." && \
	make invoke

invoke:
	endpoint=$$(jq .CdkBrefStack.Url cdk-outputs.json --raw-output) && \
	echo endpoint=$${endpoint} && \
	curl $${endpoint}?name=LocalStack!

start:
	@test -n "${LOCALSTACK_AUTH_TOKEN}" || (echo "LOCALSTACK_AUTH_TOKEN is not set. Find your token at https://app.localstack.cloud/workspace/auth-token"; exit 1)
	DEBUG=1 LOCALSTACK_AUTH_TOKEN=$(LOCALSTACK_AUTH_TOKEN) localstack start -d

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

.PHONY: usage install install-bref install-bref-docker start run invoke stop ready logs test-ci
