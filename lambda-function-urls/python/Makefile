export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION = us-east-1

usage:       ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:     ## Install dependencies
	@which awslocal || pip install awscli-local

run:         ## Build, deploy, and invoke the Lambda function URL
	npm i -g zip
	pip3 install -r requirements.txt -t .
	zip -r function.zip .
	awslocal lambda create-function \
		--function-name trending \
		--runtime python3.9 \
		--timeout 10 \
		--zip-file fileb://function.zip \
		--handler lambda_function.lambda_handler \
		--role cool-stacklifter

	awslocal lambda create-function-url-config \
		--function-name trending \
		--auth-type NONE

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
