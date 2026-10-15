export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION ?= us-east-1

usage:                  ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

run:
	./1-create-bucket.sh
	./2-build-layer.sh
	./3-deploy.sh
	./4-invoke.sh
	./5-get-traces.sh

start:
	lstk start --non-interactive --type aws
stop:
	@echo
	lstk stop

ready:
	@echo Waiting on the LocalStack container...
	@lstk status > /dev/null && echo Localstack is ready to use! || (echo Gave up waiting on LocalStack, exiting. && exit 1)

logs:
	@lstk logs > logs.txt

test-ci:
	make start install ready run; return_code=`echo $$?`;\
	make logs; make stop; exit $$return_code;
	
.PHONY: usage install run stop ready logs test-ci
