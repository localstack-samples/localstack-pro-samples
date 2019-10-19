export DOCKER_BRIDGE ?= $(shell (uname -a | grep Linux > /dev/null) && echo 172.17.0.1 || echo docker.for.mac.localhost)
export SERVICES = serverless,cloudformation,sts,stepfunctions,sqs
export START_WEB ?= 1

usage:           ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:         ## Install dependencies
	@which terraform || echo 'Please install terraform'

start:           ## Deploy and start the app locally
	terraform apply

lint:

.PHONY: usage install start lint
