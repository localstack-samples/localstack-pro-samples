export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION = us-east-1

usage:       ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:     ## Install dependencies
	@which awslocal || pip install awscli-local

run:         ## Build, deploy, and invoke the Lambda container image locally
	echo "Creating a new ECR repository locally"; \
	repoUri=$$(awslocal ecr create-repository --repository-name repo1 | jq -r '.repository.repositoryUri'); \
	echo "Building the Docker image, pushing it to ECR URL: $$repoUri"; \
	docker build -t "$$repoUri" .; \
	docker push "$$repoUri"; \
	docker rmi "$$repoUri"; \
	echo "Deploying Lambda function from container image locally"; \
	awslocal lambda create-function \
        --function-name ruby-lambda-image \
        --package-type Image \
        --code ImageUri=localhost:4510/repo1 \
		--handler app.App::Handler.process \
        --role arn:aws:iam::000000000000:role/lambda-r1; \
	sleep 10;
	echo "Invoking Lambda function from container image"; \
	awslocal lambda invoke --function-name ruby-lambda-image \
		--cli-binary-format raw-in-base64-out \
		--payload '{"test":"test"}' /tmp/lambda.out; \
	cat /tmp/lambda.out; \
	echo "Done - test successfully finished."

start:
	PROVIDER_OVERRIDE_LAMBDA=asf localstack start -d

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
	
.PHONY: usage install start run stop ready logs test-ci
