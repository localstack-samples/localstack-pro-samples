export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export SERVICES = serverless,athena
export AWS_DEFAULT_REGION=us-east-1

usage:       ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:     ## Install dependencies
	@test -e node_modules || npm install
	@which localstack || pip install localstack
	@which awslocal || pip install awscli-local

run:         ## Set up database connections and run Athena queries locally
	@make install; \
		echo "Running Athena queries"; \
		./run.sh

test-ci:
	# skip Athena tests for now, to avoid downloading large images in CI

.PHONY: usage install run
