export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION = us-east-1


check:    ## Check if all required prerequisites are installed
	@command -v docker > /dev/null 2>&1 || { echo "Docker is not installed. Please install Docker and try again."; exit 1; }
	@command -v terraform > /dev/null 2>&1 || { echo "Terraform is not installed. Please install Terraform and try again."; exit 1; }
	@command -v localstack > /dev/null 2>&1 || { echo "LocalStack CLI is not installed. Please install it and try again."; exit 1; }
	@command -v awslocal > /dev/null 2>&1 || { echo "awslocal is not installed. Please run: pip install awscli-local"; exit 1; }
	@echo "All required prerequisites are available."



init:
	terraform workspace new local &
	terraform workspace new aws &
	terraform init

build:
	docker build . --file Dockerfile-localstack --output .

build-aws:
	docker build . --file Dockerfile-aws --output .

deploy:
	docker compose up --detach
	terraform workspace select local
	AWS_ENDPOINT_URL=https://localhost.localstack.cloud:4566 terraform apply --auto-approve

deploy-aws:
	terraform workspace select aws
	terraform apply --auto-approve

run:
	terraform workspace select local
	./start_job.sh local

run-aws:
	terraform workspace select aws
	./start_job.sh aws


start:       ## Start LocalStack
	@test -n "${LOCALSTACK_AUTH_TOKEN}" || (echo "LOCALSTACK_AUTH_TOKEN is not set. Find your token at https://app.localstack.cloud/workspace/auth-token"; exit 1)
	DEBUG=1 LOCALSTACK_AUTH_TOKEN=$(LOCALSTACK_AUTH_TOKEN) localstack start -d

stop:
	docker compose down

logs:
	@localstack logs > logs.txt
	cat logs.txt

destroy:
	terraform workspace select local
	./stop-application.sh
	terraform destroy --auto-approve

destroy-aws:
	terraform workspace select aws
	./stop-application.sh aws
	terraform destroy --auto-approve

test-ci:
	make init build deploy logs run; return_code=`echo $$?`;\
	make logs; make stop; exit $$return_code;
