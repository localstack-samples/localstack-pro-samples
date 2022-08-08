export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION = us-east-1
export SERVICES = neptune
PYTHON_BIN ?= $(shell which python3 || which python)

usage:      ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:    ## Install dependencies
	@which localstack || pip install localstack
	@which awslocal || pip install awscli-local
	@pip install gremlinpython boto3

run:        ## Run the scenario with queries against local Neptune
	@$(PYTHON_BIN) query.py

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
	#make start install ready run; return_code=`echo $$?`;\
	#make logs; make stop; exit $$return_code;
	echo "SKIPPING neptune test for now, @FIXME!!"
.PHONY: usage install start run stop ready logs test-ci

