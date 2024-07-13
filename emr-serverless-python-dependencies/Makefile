init:
	terraform workspace new local &
	terraform workspace new aws &
	terraform init

build:
	docker build . --file Dockerfile-localstack --output .

build-aws:
	docker build . --file Dockerfile-aws --output .

deploy:
	# docker-compose up --detach
	terraform workspace select local
	tflocal apply --auto-approve

deploy-aws:
	terraform workspace select aws
	terraform apply --auto-approve

run:
	terraform workspace select local
	./start_job.sh local

run-aws:
	terraform workspace select aws
	./start_job.sh aws

destroy:
	terraform workspace select local
	./stop-application.sh
	terraform destroy --auto-approve

destroy-aws:
	terraform workspace select aws
	./stop-application.sh aws
	terraform destroy --auto-approve

test-ci:
	# Skipping test as resource heavy