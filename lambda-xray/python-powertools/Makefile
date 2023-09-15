export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION ?= us-east-1

usage:                  ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:                ## Install dependencies
	@which awslocal || pip install awscli-local
	@which samlocal || pip install aws-sam-cli-local

run: deploy invoke get-trace-summaries get-traces

deploy:                 ## Deploy the Lambda function
	samlocal deploy --stack-name sam-tracer-lambda --resolve-s3 --no-confirm-changeset

invoke:                 ## Invoke the Lambda function
	samlocal remote invoke --stack-name sam-tracer-lambda --event '{"charge_id": 123}'

get-trace-summaries:    ## Get the latest X-Ray trace summaries (default 10min)
	samlocal traces

watch-trace-summaries:  ## Get the latest X-Ray trace summaries (default 10min) and keep watching
	samlocal traces --tail

get-traces:             ## Get the latest X-Ray traces (default 10min)
	TIME=$$(date +%s); \
	ID=$$(awslocal xray get-trace-summaries --start-time $$(($$TIME-600)) --end-time $$TIME | jq -r '.TraceSummaries[0].Id'); \
	awslocal xray batch-get-traces --trace-ids $$ID

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
	
.PHONY: usage install run deploy invoke get-trace-summaries watch-trace-summaries get-traces stop ready logs test-ci
