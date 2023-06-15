export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION=us-east-1

usage:       ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:     ## Install dependencies
	@which localstack || pip install localstack
	@which awslocal || pip install awscli-local
	@which tflocal || pip install terraform-local
	@test -e .venv || (virtualenv .venv; . .venv/bin/activate; pip install -r requirements.txt)

run:         ## Deploy and run the sample locally
	@(test -d .terraform || tflocal init) && tflocal apply --auto-approve
	@source .venv/bin/activate && python test_stream_consumer.py &
	./ddb-data.sh

start:
	localstack start -d

clear: 		 ## remove remnants from older deployments
	@rm -f terraform.tfstate terraform.tfstate.backup

clean: clear	 ## remove all project related files and reverse terraform init
	@rm -f -r .terraform .terraform.lock.hcl

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

