export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export SERVICES = s3,transfer
export AWS_DEFAULT_REGION=us-east-1

usage:       ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:     ## Install dependencies
	@npm install
	@which localstack || pip install localstack
	@which awslocal || pip install awscli-local
	@test -e .venv || (virtualenv .venv; . .venv/bin/activate; pip install -r requirements.txt)

run:         ## Deploy and run the sample locally
	@echo "Running Test: Creating FTP server and uploading files to S3 via Transfer API"; \
		(. .venv/bin/activate; python test.py)

test-ci:
	make install && make run || true

.PHONY: usage install run
