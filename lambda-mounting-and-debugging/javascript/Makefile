export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION = us-east-1
VENV_DIR ?= .venv

usage:       ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:     ## Install dependencies
	@which awslocal || pip install awscli-local
	test -e $(VENV_DIR) || virtualenv $(VENV_DIR)
	. $(VENV_DIR)/bin/activate; pip install debugpy

run:         ## Deploy and invoke the Lambda container locally
	echo "Deploying Lambda locally"; \
	./run.sh; \
	echo "Done - test successfully finished."

start:
	docker-compose up -d

stop:
	@echo
	localstack stop
ready:
	@echo Waiting on the LocalStack container...
	@localstack wait -t 30 && echo Localstack is ready to use! || (echo Gave up waiting on LocalStack, exiting. && exit 1)

logs:
	@localstack logs > logs.txt
	
.PHONY: usage install start run stop ready logs test-ci
