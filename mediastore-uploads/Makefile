export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION = us-east-1

usage:      ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:    ## Install dependencies
	@which localstack > /dev/null || pip install localstack
	@which awslocal > /dev/null || pip install awscli-local

run:        ## Run tests uploading objects via MediaStore API
	./test.sh

start:
	localstack start -d

stop:
	localstack stop

ready:
	@localstack wait -t 30; echo "Localstack is ready to use!"

test-ci:
	make start install ready run stop

.PHONY: usage install run
