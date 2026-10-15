export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION=us-east-1

usage:       
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

check:    ## Check if all required prerequisites are installed
	@command -v docker > /dev/null 2>&1 || { echo "Docker is not installed. Please install Docker and try again."; exit 1; }
	@command -v aws > /dev/null 2>&1 || { echo "AWS CLI is not installed (required by 'lstk aws'). Please install it and try again."; exit 1; }
	@echo "All required prerequisites are available."


install:     

run:         
	./run.sh

start:
	@test -n "${LOCALSTACK_AUTH_TOKEN}" || (echo "LOCALSTACK_AUTH_TOKEN is not set. Find your token at https://app.localstack.cloud/workspace/auth-token"; exit 1)
	DEBUG=1 LOCALSTACK_AUTH_TOKEN=$(LOCALSTACK_AUTH_TOKEN) docker compose up -d

stop:
	@echo
	docker compose down

ready:
	@echo Waiting on the LocalStack container...
	@for i in $$(seq 1 120); do curl -sf http://localhost:4566/_localstack/health > /dev/null && break; sleep 1; done; \
		curl -sf http://localhost:4566/_localstack/health > /dev/null && echo Localstack is ready to use! || (echo Gave up waiting on LocalStack, exiting. && exit 1)

logs:
	@docker compose logs localstack > logs.txt

test-ci:
	make start install ready run; return_code=`echo $$?`;\
	make logs; make stop; exit $$return_code;
	
.PHONY: usage install start run stop ready logs test-ci
