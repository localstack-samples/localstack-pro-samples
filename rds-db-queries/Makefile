export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION = us-east-1
export SERVICES = rds
SHELL := /bin/bash
PYTHON_BIN ?= $(shell which python3 || which python)

usage:      ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:    ## Install dependencies
	@which localstack || pip install localstack
	@which awslocal || pip install awscli-local
	@test -e .venv || ($(PYTHON_BIN) -m venv .venv; source .venv/bin/activate; pip install psycopg2 boto3)

run:        ## Run the scenario with the DB queries against local RDS
	@source .venv/bin/activate && $(PYTHON_BIN) query.py

test-ci:
	make install && make run || true

.PHONY: usage install run
