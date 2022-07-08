export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export SERVICES = serverless,appsync,dynamodb,rds,secretsmanager
export AWS_DEFAULT_REGION=us-east-1
APPSYNC_URL = http://localhost:4566/graphql
SHELL := /bin/bash

usage:       ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:     ## Install dependencies
	@test -e node_modules || npm install
	@which serverless || npm install -g serverless
	@which localstack || pip install localstack
	@which awslocal || pip install awscli-local
	@test -e .venv || (python3 -m venv .venv; source .venv/bin/activate; pip install -r requirements.txt)

run:         ## Deploy the app locally and run an AppSync GraphQL test invocation
	@make install; \
	./run.sh

test-ci:
	make install && make run

.PHONY: usage install start lint
