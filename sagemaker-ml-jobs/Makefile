export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION = us-east-1
export SERVICES = sagemaker,s3,logs,sts,iam
PYTHON_BIN ?= $(shell which python3 || which python)

usage:      ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:    ## Install dependencies
	@which localstack || pip install localstack
	@which awslocal || pip install awscli-local
	@test -e .venv || virtualenv --python $(PYTHON_BIN) .venv
	@. .venv/bin/activate; pip install tensorflow==1.15.0 sagemaker localstack 'requests>=2.20.0'

run:        ## Launch the TensorFlow training job in local SageMaker
	@. .venv/bin/activate; python run_job.py

test-ci:
	# disable for now, to avoid downloading large dependencies in CI

.PHONY: usage install run
