export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export SERVICES = serverless,iot
export AWS_DEFAULT_REGION=us-east-1

usage:       ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:     ## Install dependencies
	@npm install
	@which localstack || pip install localstack
	@which awslocal || pip install awscli-local
	@test -e .venv || (virtualenv .venv; . .venv/bin/activate; pip install -r requirements.txt)

test-mqtt:
	@echo 'Running MQTT publish/subscribe test'; \
		(. .venv/bin/activate; python mqtt_test.py)

run:         ## Deploy the app locally
	@make install; \
		echo "Deploying app to local environment"; \
		awslocal cloudformation create-stack --stack-name test-iot --template-body file://iot.cf.yml; \
		echo "IoT stack successfully deployed. Now checking whether all resources have been created."; \
		awslocal iot list-things; \
		awslocal iot list-policies; \
		awslocal iot create-job --job-id j1 --targets t1; \
		awslocal iot list-jobs; \
		make test-mqtt

test-ci:
	make install && make run

.PHONY: usage install run
