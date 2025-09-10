.PHONY: usage install build build-docker build-local build-sam wait deploy deploy-aws deploy-sam invoke clean start stop ready test-ci

AWS_ENDPOINT_URL ?= http://localhost.localstack.cloud:4566
AWS ?= AWS_ENDPOINT_URL=$(AWS_ENDPOINT_URL) \
	AWS_ACCESS_KEY_ID=test \
	AWS_SECRET_ACCESS_KEY=test \
	AWS_DEFAULT_REGION=us-east-1 \
	aws
SAM ?= AWS_ENDPOINT_URL=$(AWS_ENDPOINT_URL) \
	AWS_ACCESS_KEY_ID=test \
	AWS_SECRET_ACCESS_KEY=test \
	AWS_DEFAULT_REGION=us-east-1 \
	sam
FUNCTION_NAME ?= HelloWorldFunctionJava
LAMBDA_RUNTIME ?= java21

ARCH ?= x86_64
DOCKER_PLATFORM ?= linux/$(ARCH)
IMAGE ?= public.ecr.aws/sam/build-$(LAMBDA_RUNTIME):latest-$(ARCH)

all: usage

usage:                ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

# TODO: figure out how to install the AWS CLI v2 in CI
install:              ## Install CLI dependencies
	@which aws || pip install awscli

build: build-docker   ## Build the Lambda function (default Docker)

build-docker:         ## Build the Lambda function zip in Docker
	docker run --platform $(DOCKER_PLATFORM) --rm -v "$$(pwd)/HelloWorldFunction:/app" $(IMAGE) bash -c "cd /app && ./gradlew test buildZip && mv build/distributions/app.zip build/distributions/HelloWorldFunction.zip"

build-local:          ## Build the Lambda function zip locally (JDK required)
	cd HelloWorldFunction && ./gradlew test buildZip

build-sam:            ## Build the Lambda function via AWS SAM
	$(SAM) build --use-container

wait:                 ## Wait until the Lambda function becomes ready to invoke
	$(AWS) lambda wait function-active-v2 --function-name $(FUNCTION_NAME)

deploy: deploy-aws    ## Deploy the Lambda function (default AWS CLI)

deploy-aws:           ## Deploy the Lambda function via AWS CLI
	$(AWS) lambda create-function \
	--function-name $(FUNCTION_NAME) \
	--runtime $(LAMBDA_RUNTIME) \
	--role arn:aws:iam::000000000000:role/lambda-role \
	--handler helloworld.App::handleRequest \
	--zip-file fileb://HelloWorldFunction/build/distributions/HelloWorldFunction.zip \
	--memory-size 512 \
	--timeout 2

deploy-sam:           ## Deploy the Lambda function via AWS SAM CLI
	$(SAM) deploy

invoke:               ## Invoke the Lambda function and show logs
	AWS_MAX_ATTEMPTS=1 $(AWS) lambda invoke --function-name $(FUNCTION_NAME) \
	--payload file://events/event.json \
	--cli-connect-timeout 3600 \
	--cli-read-timeout 3600 \
	--log-type Tail \
	response.json | jq .LogResult -r | base64 -d && cat response.json | jq -r .result

clean:                ## Clean the build directory
	rm -rf HelloWorldFunction/build

start:                ## Start LocalStack
	IMAGE_NAME=localstack/localstack-pro \
	LOCALSTACK_AUTH_TOKEN=${LOCALSTACK_AUTH_TOKEN} \
	LOCALSTACK_LAMBDA_DEBUG_MODE=1 \
	LOCALSTACK_LAMBDA_DEBUG_MODE_CONFIG_PATH=/tmp/lambda_debug_mode_config.yaml \
	localstack start --detached --volume ${PWD}/lambda_debug_mode_config.yaml:/tmp/lambda_debug_mode_config.yaml

stop:                 ## Stop LocalStack
	localstack stop

ready:                ## Wait until LocalStack is running
	@echo Waiting on the LocalStack container...
	@localstack wait -t 30 && echo LocalStack is ready to use! || (echo Gave up waiting on LocalStack, exiting. && exit 1)

test-ci:
	make start install ready deploy wait invoke; return_code=`echo $$?`;\
	echo "Interactive debugging not tested in CI"; exit $$return_code;
