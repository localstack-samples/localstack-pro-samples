export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export SERVICES = cloudformation,mediastore
export AWS_DEFAULT_REGION = us-east-1

usage:      ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:    ## Install dependencies
	@which localstack > /dev/null || pip install localstack
	@which awslocal > /dev/null || pip install awscli-local

run:        ## Run tests uploading objects via MediaStore API
	@make install; \
		./test.sh

test-ci:
	make install && make run

.PHONY: usage install run
