export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION=us-east-1

usage:       ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:     ## Install dependencies
	@which localstack || pip install localstack
	@which awslocal || pip install awscli-local
	@test -e .venv || (virtualenv .venv; . .venv/bin/activate; pip install -r requirements.txt)

test-mqtt:
	@echo 'Running MQTT publish/subscribe test'; \
		(. .venv/bin/activate; python mqtt_test.py)

run:         ## Deploy the app locally
	echo "Deploying app to local environment"; \
	awslocal cloudformation create-stack --stack-name test-iot --template-body file://iot.cf.yml; \
	echo "IoT stack successfully deployed. Now checking whether all resources have been created."; \
	sleep 3; \
	awslocal iot list-things; \
	awslocal iot list-policies; \
	awslocal iot create-job --job-id j1 --targets t1; \
	awslocal iot list-jobs; \
	make test-mqtt

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
	
.PHONY: usage install test-mqtt start run stop ready logs test-ci

