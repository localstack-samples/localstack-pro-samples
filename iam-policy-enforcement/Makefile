export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export SERVICES = serverless,iot
export AWS_DEFAULT_REGION=us-east-1

usage:       ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:     ## Install dependencies
	@which localstack || pip install localstack
	@which awslocal || pip install awscli-local

run:         ## Run the IAM tests locally
	@make install
	@echo "Running IAM enforcement tests in local environment"
	@./run.sh

test-ci:
	make install && make run || true

.PHONY: usage install run
