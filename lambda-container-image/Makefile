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
	awslocal lambda create-function --function-name ls-lambda-image --package-type Image \
		--code ImageUri=$$repoUri --role arn:aws:iam::000000000:role/lambda-r1 \
		--handler handler.handler; \
	echo "Invoking Lambda function from container image"; \
	awslocal lambda invoke --function-name ls-lambda-image --payload '{"test":"test"}' /tmp/lambda.out; \
	echo "Done - test successfully finished."

start:
	localstack start -d

stop:
	localstack stop

ready:
	@localstack wait -t 30; echo "Localstack is ready to use!"

test-ci:
	make start install ready run stop

.PHONY: usage install deploy
