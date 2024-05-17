export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION = us-east-1
SHELL := /bin/bash
PYTHON_BIN ?= $(shell which python3 || which python)

usage:       ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

start:
	localstack start -d

install:    ## Install dependencies
	@which localstack || pip install localstack
	@which awslocal || pip install awscli-local
	@which terraform || (\
	echo 'Terraform was not found, installing locally' && \
	wget https://releases.hashicorp.com/terraform/1.0.8/terraform_1.0.8_linux_amd64.zip && \
	unzip terraform_*.zip && \
	rm terraform_*.zip)
	@test -e .venv || ($(PYTHON_BIN) -m venv .venv; source .venv/bin/activate; pip3 install terraform-local;)

package:
	source .venv/bin/activate; pip install \
	--platform manylinux2014_x86_64 \
	--target=package \
	--implementation cp \
	--only-binary=:all: \
	--upgrade \
	--requirement requirements.txt \
	--target build/my-lambda-layer/python

init:
	tflocal init

deploy:
	tflocal apply --auto-approve

invoke:
	awslocal lambda invoke \
    --function-name my-lambda-function \
    output.json
	cat output.json

run: start install init deploy invoke

clean:
	rm -rf build
	rm -rf .terraform
	rf -f output.json

.PHONY: start install init deploy invoke clean
