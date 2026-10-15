
check:    ## Check if all required prerequisites are installed
	@command -v docker > /dev/null 2>&1 || { echo "Docker is not installed. Please install Docker and try again."; exit 1; }
	@command -v lstk > /dev/null 2>&1 || { echo "lstk CLI is not installed. Please run: npm install -g @localstack/lstk"; exit 1; }
	@command -v awslocal > /dev/null 2>&1 || { echo "awslocal is not installed. Please run: pip install awscli-local"; exit 1; }
	@echo "All required prerequisites are available."


# Install requirements
install:    
	docker pull ubuntu:focal
	docker tag ubuntu:focal localstack-ec2/ubuntu-focal-docker-ami:ami-00a001

# Run demo
run:
	./run.sh


start:
	@test -n "${LOCALSTACK_AUTH_TOKEN}" || (echo "LOCALSTACK_AUTH_TOKEN is not set. Find your token at https://app.localstack.cloud/workspace/auth-token"; exit 1)
	LOCALSTACK_EC2_VM_MANAGER=docker LOCALSTACK_DEBUG=1 LOCALSTACK_AUTH_TOKEN=$(LOCALSTACK_AUTH_TOKEN) lstk start --non-interactive --type aws

stop:
	@echo
	lstk stop
ready:
	@echo Waiting on the LocalStack container...
	@lstk status > /dev/null && echo Localstack is ready to use! || (echo Gave up waiting on LocalStack, exiting. && exit 1)

logs:
	@lstk logs > logs.txt

test-ci:
	make start install ready run; return_code=`echo $$?`;\
	make logs; make stop; exit $$return_code;

.PHONY: install start run stop ready logs test-ci
