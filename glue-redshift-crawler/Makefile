export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION = us-east-1

usage:     ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:   ## Install dependencies
	@which localstack || pip install localstack
	@which awslocal || pip install awscli-local
	docker pull localstack/bigdata

run:    ## Prepare environment and run sample
	./run.sh

start:
	localstack start -d

stop:
	localstack stop

ready:
	@localstack wait -t 30; echo "Localstack is ready to use!"

test-ci:
	make start install ready run stop

.PHONY: usage install run test-ci
