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
		SLS_DEBUG=1 npm run deploy && \
		echo "Serverless app successfully deployed. Now invoking the Lambda function to generate XRay traces." && \
		awslocal lambda invoke --function-name test-xray-local-hello /tmp/out.tmp; \
		TIME=$$(date +%s); \
		ID=$$(awslocal xray get-trace-summaries --start-time $$(($$TIME-120)) --end-time $$TIME | jq -r '.TraceSummaries[0].Id'); \
		awslocal xray batch-get-traces --trace-ids $$ID

.PHONY: usage install run
