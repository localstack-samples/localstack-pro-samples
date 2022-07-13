export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export DOCKER_BRIDGE ?= $(shell (uname -a | grep Linux > /dev/null) && echo 172.17.0.1 || echo docker.for.mac.localhost)
export SERVICES = edge,serverless,cloudformation,sts,stepfunctions,sqs
export START_WEB ?= 1

usage:           ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:         ## Install dependencies
	@npm install
	@which serverless || npm install -g serverless
	@which localstack || pip install localstack

run:           ## Deploy and start the app locally
	@make install; \
		echo "Deploying Serverless app to local environment"; \
		SLS_DEBUG=1 serverless deploy --stage local && \
		echo "Serverless app successfully deployed. Please open the file demo/web/index.html in your browser."

lint:            ## Run code linter
	@npm run lint
	@flake8 demo

check:
	@test $${LOCALSTACK_API_KEY+x} || (echo 'Please configure $$LOCALSTACK_API_KEY with your API key'; exit 1)

test-ci:
	# skip this test in CI for now

.PHONY: usage install start lint
