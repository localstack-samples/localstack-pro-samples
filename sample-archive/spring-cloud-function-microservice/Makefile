BUILD_FOLDER ?= build
SOURCES_FOLDER ?= src
HOT_RELOADABLE_FOLDER ?= build/hot

export AWS_REGION ?= us-east-1
export LAMBDA_MOUNT_CWD ?= $(shell pwd)/$(HOT_RELOADABLE_FOLDER)

usage:                       ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/:.*##\s*/##/g' | awk -F'##' '{ printf "%-20s %s\n", $$1, $$2 }'

build:                       ## Make a full build with fat jar
	./gradlew build

build-jar:                   ## Build a fat jar only
	./gradlew shadowJar

build-hot:                   ## Build and prepare the codebase for hot swapping
	./gradlew buildHot

watch:                       ## Watch project files to perform hot swapping
	bin/watchman.sh $(SOURCES_FOLDER) "make build-hot"

deploy-sls: build-jar        ## Deploy serverless project to a specified stage
	cd deployments/serverless && npm install && npm run deploy -- --stage $(STAGE)

deploy-sls-local: build-hot  ## Deploy serverless project to LocalStack and enable hot-swapping
	cd deployments/serverless && npm install && npm run deploy -- --stage local

deploy-cdk-local: build-hot  ## Deploy serverless project to LocalStack and enable hot-swapping
	cd deployments/cdk && \
        cdklocal bootstrap aws://000000000000/$(AWS_REGION) && \
        cdklocal deploy

deploy-tf-local: build-hot  ## Deploy serverless project to LocalStack and enable hot-swapping
	cd deployments/terraform && \
        terraform init && \
        terraform apply -var "STAGE=local" -var "AWS_REGION=$(AWS_REGION)" -var "LAMBDA_MOUNT_CWD=$(LAMBDA_MOUNT_CWD)"


clean:                      ## Clean up
	rm -rf build

.PHONY: usage build build-jar build-hot watch deploy-sls deploy-sls-local deploy-cdk-local deploy-tf-local clean
