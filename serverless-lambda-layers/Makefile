export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION = us-east-1

usage:       ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:     ## Install dependencies
	@npm install
	@which serverless || npm install -g serverless
	@npm install --save-dev serverless-localstack
	@which localstack || pip install localstack
	@which awslocal || pip install awscli-local

run:         ## Deploy the app locally and run a Lambda test invocation
	echo "Deploying Serverless app to local environment"; \
	awslocal s3api create-bucket --bucket testbucket --region us-east-1; \
	SLS_DEBUG=1 npm run deploy && \
	echo "Serverless app successfully deployed. Now trying to invoke the Lambda function with layer." && \
	awslocal lambda invoke --function-name test-layers-local-hello /tmp/out.tmp

start:
	localstack start -d

stop:
	@echo
	localstack stop
ready:
	@echo Waiting on the LocalStack container...
	@localstack wait -t 30 && echo Localstack is ready to use! || (echo Gave up waiting on LocalStack, exiting. && exit 1)

logs:
	@localstack logs > logs.txt

test-ci:
	make start install ready run; return_code=`echo $$?`;\
	make logs; make stop; exit $$return_code;
	
.PHONY: usage install start run stop ready logs test-ci

