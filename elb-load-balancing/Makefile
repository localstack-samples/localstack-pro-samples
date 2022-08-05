export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION = us-east-1
export SERVICES = serverless,events,cognito

usage:       ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:     ## Install dependencies
	@npm install
	@which serverless || npm install -g serverless
	@which localstack || pip install localstack
	@which awslocal || pip install awscli-local

run:         ## Deploy the app locally and run a Lambda test invocation
	echo "Deploying Serverless app to local environment"; \
	awslocal s3api create-bucket --bucket testbucket; \
	SLS_DEBUG=1 npm run deploy && \
	echo "Serverless app successfully deployed. Now trying to invoke the Lambda functions via ELB endpoint." && \
	echo && echo "Invoking endpoint 1: http://lb-test-1.elb.localhost.localstack.cloud:4566/hello1" && \
	curl http://lb-test-1.elb.localhost.localstack.cloud:4566/hello1 && \
	echo && echo && echo "Invoking endpoint 2: http://lb-test-1.elb.localhost.localstack.cloud:4566/hello2" && \
	curl http://lb-test-1.elb.localhost.localstack.cloud:4566/hello2


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

