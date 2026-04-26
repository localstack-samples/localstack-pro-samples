export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION ?= us-east-1
SHELL := /bin/bash
TERRAFORM_VERSION ?= 1.11.4

usage:       ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

check:       ## Check if all required prerequisites are installed
	@command -v docker > /dev/null 2>&1 || { echo "Docker is not installed. Please install Docker and try again."; exit 1; }
	@command -v localstack > /dev/null 2>&1 || { echo "LocalStack CLI is not installed. Please install it and try again."; exit 1; }
	@command -v terraform > /dev/null 2>&1 || { echo "Terraform is not installed. Please install Terraform and try again."; exit 1; }
	@test -x python/node_modules/.bin/cdktf || command -v cdktf > /dev/null 2>&1 || { echo "cdktf is not installed. Please run: cd python && npm ci"; exit 1; }
	@command -v pipenv > /dev/null 2>&1 || { echo "pipenv is not installed. Please run: pip install pipenv"; exit 1; }
	@echo "All required prerequisites are available."

install:     ## Install dependencies
	@cd python && npm ci
	@cd python && pipenv install
	@cd python && npx cdktf get

install-ci-dependencies: ## Install CI-only prerequisites
	@python -m pip install pipenv
	@if ! command -v terraform > /dev/null 2>&1; then \
		tmp_dir=$$(mktemp -d); \
		curl -fsSL "https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip" -o "$$tmp_dir/terraform.zip"; \
		unzip -q "$$tmp_dir/terraform.zip" -d "$$tmp_dir"; \
		sudo install -m 0755 "$$tmp_dir/terraform" /usr/local/bin/terraform; \
		rm -rf "$$tmp_dir"; \
	fi

start:       ## Start LocalStack
	@test -n "${LOCALSTACK_AUTH_TOKEN}" || (echo "LOCALSTACK_AUTH_TOKEN is not set. Find your token at https://app.localstack.cloud/workspace/auth-token"; exit 1)
	localstack start -d

stop:        ## Stop LocalStack
	@echo
	localstack stop

ready:       ## Wait until LocalStack is ready
	@echo Waiting on the LocalStack container...
	@localstack wait -t 30 && echo LocalStack is ready to use! || (echo Gave up waiting on LocalStack, exiting. && exit 1)

logs:        ## Retrieve LocalStack logs
	@localstack logs > logs.txt

deploy:      ## Deploy CDK for Terraform stack
	@cd python && npx cdktf deploy --auto-approve

run:         ## Run the deployed stack (alias for deploy)
	make deploy

test-ci:     ## Run CI tests
	make install-ci-dependencies install check start ready deploy; return_code=`echo $$?`;\
	make logs; make stop; exit $$return_code;

.PHONY: usage check install install-ci-dependencies start stop ready logs deploy run test-ci
