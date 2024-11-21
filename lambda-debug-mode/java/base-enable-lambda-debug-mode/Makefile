export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION = us-east-1
VENV_DIR ?= .venv

# https://hub.docker.com/_/gradle/tags
IMAGE ?= gradle:8.4.0-jdk17

usage:       ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install: build-docker

build-docker: ## Build the Lambda function zip in Docker
	docker run --rm -v "$$(pwd)/java-function:/app" $(IMAGE) bash -c "cd /app && ./gradlew buildZip"

build-local: ## Build the Lambda function zip locally
	cd java-function && ./gradlew buildZip

clean:
	rm -rf java-function/build

run:         ## Deploy and invoke the Lambda container locally
	echo "Deploying Lambda locally"; \
	./run.sh; \
	echo "Done - test successfully finished."

start:
	LOCALSTACK_LAMBDA_DEBUG_MODE=1 \
	LOCALSTACK_LAMBDA_DEBUG_MODE_CONFIG_PATH=/tmp/lambda_debug_mode_config.yaml \
	localstack start --volume ${PWD}/lambda_debug_mode_config.yaml:/tmp/lambda_debug_mode_config.yaml -d

stop:
	@echo
	localstack stop

ready:
	@echo Waiting on the LocalStack container...
	@localstack wait -t 30 && echo Localstack is ready to use! || (echo Gave up waiting on LocalStack, exiting. && exit 1)

logs:
	@localstack logs > logs.txt

test-ci:
	make install; return_code=`echo $$?`;\
	echo "Interactive debugging not tested in CI"; exit $$return_code;

.PHONY: usage install run start stop ready logs test-ci build-local build-docker clean
