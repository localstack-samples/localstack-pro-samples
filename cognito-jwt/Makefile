export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION = us-east-1
export SERVICES = cognito

usage:      ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:    ## Install dependencies
	@which localstack || pip install localstack
	@which awslocal || pip install awscli-local

run:        ## Run the scenario with the Cognito commands
	@./test.sh

test-ci:
	# skip cognito tests in CI for now, as they require interactive input

.PHONY: usage install run test-ci
