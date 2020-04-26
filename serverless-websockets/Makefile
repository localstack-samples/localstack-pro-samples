export VENV_DIR ?= .venv
export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION = us-east-1
export SERVICES = serverless,apigatewayv2

usage:       ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:     ## Install dependencies
	@npm install
	@which serverless || npm install -g serverless
	@which localstack || pip install localstack
	@which awslocal || pip install awscli-local
	@test -e $(VENV_DIR) || virtualenv $(VENV_DIR)
	@. $(VENV_DIR)/bin/activate; pip install -r requirements.txt

run:         ## Deploy and run the app locally
	@make install; \
		echo "Deploying Serverless app to local environment"; \
		SLS_DEBUG=1 npm run deploy; \
		echo "Starting client that connects to Websocket API"; \
		. $(VENV_DIR)/bin/activate; python test.py

test-ci:
	make install && make run || true

.PHONY: usage install run
