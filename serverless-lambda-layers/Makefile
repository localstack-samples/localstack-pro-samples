export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export SERVICES = serverless
export AWS_DEFAULT_REGION=us-east-1

usage:       ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:     ## Install dependencies
	@npm install
	@which serverless || npm install -g serverless
	@which localstack || pip install localstack
	@which awslocal || pip install awscli-local

run:         ## Deploy the app locally and run a Lambda test invocation
	@make install; \
		echo "Deploying Serverless app to local environment"; \
		awslocal s3api create-bucket --bucket testbucket; \
		SLS_DEBUG=1 npm run deploy && \
		echo "Serverless app successfully deployed. Now trying to invoke the Lambda function with layer." && \
		awslocal lambda invoke --function-name test-layers-local-hello /tmp/out.tmp

.PHONY: usage install start lint
