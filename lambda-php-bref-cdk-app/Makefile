export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION ?= us-east-1

# Using composer Docker image to avoid local PHP dependency:
# https://hub.docker.com/_/composer
DOCKER_COMPOSER_IMAGE ?= composer:2.5

usage:       ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

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
	PROVIDER_OVERRIDE_lambda=v2 localstack start -d

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
