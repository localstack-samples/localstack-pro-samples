export DEBUG=1

SHELL := /bin/bash

usage:       ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:     ## Install dependencies
	@which localstack || pip install localstack
	@which awslocal || pip install awscli-local

run:         ## Run MWAA ETL Processor
	./run.sh

start:       ## Start LocalStack
	@if [ -z `docker network ls --filter name=localstack -q` ]; then \
		echo "Creating localstack network"; \
		docker network create --attachable localstack; \
	fi
	DOCKER_FLAGS='--network localstack --name=localhost.localstack.cloud -e GATEWAY_SERVER=hypercorn' localstack start -d

stop:        ## Stop LocalStack
	@echo
	MAIN_CONTAINER_NAME=localhost.localstack.cloud localstack stop
	docker rm -f $$(docker network inspect localstack | jq -r '.[0].Containers | keys[0]')

ready:       ## Wait for LocalStack to be ready
	@echo Waiting on the LocalStack container...
	@localstack wait -t 30 && echo Localstack is ready to use! || (echo Gave up waiting on LocalStack, exiting. && exit 1)

logs:        ## Retrieve logs from LocalStack
	@localstack logs > logs.txt

test-ci:     ## Run CI test
	make start install ready run; return_code=`echo $$?`;\
	make logs; make stop; exit $$return_code;

.PHONY: usage install start run stop ready logs test-ci
