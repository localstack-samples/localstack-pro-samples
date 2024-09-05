export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION = us-east-1

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

stop:
	docker compose down

logs:
	@localstack logs > logs.txt

destroy:
	terraform workspace select local
	./stop-application.sh
	terraform destroy --auto-approve

destroy-aws:
	terraform workspace select aws
	./stop-application.sh aws
	terraform destroy --auto-approve

test-ci:
	make init build deploy run; return_code=`echo $$?`;\
	make logs; make stop; exit $$return_code;
