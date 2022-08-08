export DOCKER_BRIDGE ?= $(shell (uname -a | grep Linux > /dev/null) && echo 172.17.0.1 || echo docker.for.mac.localhost)
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
	

run:           ## Deploy and start the app locally
	@(test -d .terraform || terraform init) && terraform apply --auto-approve

clear: 		 ## remove remnants from older deployments
	@rm -f terraform.tfstate terraform.tfstate.backup

clean: clear	 ## remove all project related files and reverse terraform init
	@rm -f -r .terraform .terraform.lock.hcl

uninstall:
	@rm -f terraform

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
	
.PHONY: usage install uninstall clear clean start run stop ready logs test-ci

