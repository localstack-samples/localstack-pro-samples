export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION = us-east-1
DOCKER_CONTAINER = localstack_nginx_1_0

usage:       ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

check:    ## Check if all required prerequisites are installed
	@command -v docker > /dev/null 2>&1 || { echo "Docker is not installed. Please install Docker and try again."; exit 1; }
	@command -v lstk > /dev/null 2>&1 || { echo "lstk CLI is not installed. Please run: npm install -g @localstack/lstk"; exit 1; }
	@command -v aws > /dev/null 2>&1 || { echo "AWS CLI is not installed (required by 'lstk aws'). Please install it and try again."; exit 1; }
	@echo "All required prerequisites are available."


install:     ## Install dependencies
	@which lstk > /dev/null || npm install -g @localstack/lstk

run:      ## Build and deploy the app locally
		echo "Creating a new ECR repository locally"; \
		repoUri=$$(lstk aws ecr create-repository --repository-name repo1 | jq -r '.repository.repositoryUri'); \
		echo "Building the Docker image, pushing it to local ECR URL: $$repoUri"; \
		sleep 3; \
		docker build -t "$$repoUri" .; \
		docker push "$$repoUri"; \
		docker rmi "$$repoUri"; \
		echo "Creating ECS infrastructure locally"; \
		lstk aws cloudformation create-stack --stack-name infra --template-body file://templates/ecs.infra.yml && \
		lstk aws cloudformation wait stack-create-complete --stack-name infra && \
		echo "Deploying ECS app to local environment"; \
		lstk aws cloudformation create-stack --stack-name sample \
			--template-body file://templates/ecs.sample.yml \
			--parameters ParameterKey=ImageUrl,ParameterValue=$$repoUri && \
		lstk aws cloudformation wait stack-create-complete --stack-name sample && \
		echo "ECS app successfully deployed. Trying to access app endpoint." && \
		cluster_arn=$$(lstk aws ecs list-clusters | jq -r '.clusterArns[0]') && \
		for i in {1..5}; do task_arn=$$(lstk aws ecs list-tasks --cluster $$cluster_arn | jq -r '.taskArns[0]'); if [ "$$task_arn" != "null" ]; then break; fi; sleep 2; done && \
		for i in {1..5}; do app_port=$$(lstk aws ecs describe-tasks --cluster $$cluster_arn --tasks $$task_arn | jq -r '.tasks[0].containers[0].networkBindings[0].hostPort'); if [ "$$app_port" != "null" ]; then break; fi; sleep 2; done && \
		echo "curling localhost:$$app_port" && \
		curl localhost:$$app_port && \
		echo "Sample app (nginx) successfully deployed. You can access it under http://localhost:$$app_port"

clean:        ## stop and remove created containers
	@((docker stop $(DOCKER_CONTAINER) && docker rm $(DOCKER_CONTAINER))>/dev/null 2>/dev/null) ||:

start:
	@test -n "${LOCALSTACK_AUTH_TOKEN}" || (echo "LOCALSTACK_AUTH_TOKEN is not set. Find your token at https://app.localstack.cloud/workspace/auth-token"; exit 1)
	LOCALSTACK_DEBUG=1 LOCALSTACK_AUTH_TOKEN=$(LOCALSTACK_AUTH_TOKEN) lstk start --non-interactive --type aws

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
	
.PHONY: usage install start run stop clean ready logs test-ci

