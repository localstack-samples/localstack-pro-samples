export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION = us-east-1

usage:     ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:   ## Install dependencies
	@which localstack || pip install localstack
	@which awslocal || pip install awscli-local

run-interactive: install  ## Prepare environment and run sample Glue MSK environment (interactive example)
	./run.sh -it

run run-quiet: install    ## Prepare environment and run sample Glue MSK environment (non-interactive example)
	./run.sh

test-ci:
	make install && make run

.PHONY: usage install run-interactive run-quiet run run-quiet