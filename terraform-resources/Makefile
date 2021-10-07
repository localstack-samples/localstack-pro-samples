export DOCKER_BRIDGE ?= $(shell (uname -a | grep Linux > /dev/null) && echo 172.17.0.1 || echo docker.for.mac.localhost)
export SERVICES = serverless,cloudformation,sts,stepfunctions,sqs
export START_WEB ?= 1
export PATH := $(PATH):.

usage:           ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:         ## Install dependencies
	@which terraform || (\
	echo 'Terraform was not found, installing locally' && \
	wget https://releases.hashicorp.com/terraform/1.0.8/terraform_1.0.8_linux_amd64.zip && \
	unzip terraform_*.zip && \
	rm terraform_*.zip)
	

start:           ## Deploy and start the app locally
	@(test -d .terraform || terraform init) && terraform apply

clear: 		 ## remove remnants from older deployments
	@rm -f terraform.tfstate terraform.tfstate.backup

clean: clear	 ## remove all project related files and reverse terraform init
	@rm -f -r .terraform .terraform.lock.hcl

uninstall:
	@rm -f terraform

test-ci:
	# TODO install terraform and enable in CI

.PHONY: usage install start test-ci
