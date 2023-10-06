export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION=us-east-1

usage:       ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:     ## Install dependencies
#	@npm install
	@which localstack || pip install localstack
	@which awslocal || pip install awscli-local
	@test -e .venv || (virtualenv .venv; . .venv/bin/activate; pip install -r requirements.txt)

run:         ## Deploy and run the sample locally
	@echo "Running Test: Creating FTP server and uploading files to S3 via Transfer API"; \
		(. .venv/bin/activate; python test.py)

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
	make install start ready run; return_code=`echo $$?`;\
	make logs; make stop; exit $$return_code;
	
.PHONY: usage install start run stop ready logs test-ci

