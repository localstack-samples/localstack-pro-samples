export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION ?= us-east-1

usage:       ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

check:    ## Check if all required prerequisites are installed
	@command -v docker > /dev/null 2>&1 || { echo "Docker is not installed. Please install Docker and try again."; exit 1; }
	@command -v node > /dev/null 2>&1 || { echo "Node.js is not installed. Please install Node.js and try again."; exit 1; }
	@command -v aws > /dev/null 2>&1 || { echo "AWS CLI is not installed. Please install AWS CLI and try again."; exit 1; }
	@command -v python > /dev/null 2>&1 || { echo "Python is not installed. Please install Python and try again."; exit 1; }
	@command -v openssl > /dev/null 2>&1 || { echo "OpenSSL is not installed. Please install OpenSSL and try again."; exit 1; }
	@command -v localstack > /dev/null 2>&1 || { echo "LocalStack is not installed. Please install LocalStack and try again."; exit 1; }
	@echo "All required prerequisites are available."

install:     ## Install dependencies
	@which serverless || npm install -g serverless
	@which awslocal || pip install awscli-local
	@if [ ! -d "node_modules" ]; then \
		echo "node_modules not found. Running npm install..."; \
		npm install; \
	else \
		echo "node_modules already installed."; \
	fi
	@echo "All required dependencies are available."

cert:        ## Create test SSL certificate
	@echo "Creating SSL certificates directory..."
	@mkdir -p sslcert
	@echo "Generating SSL certificate..."
	@cd sslcert; \
		which openssl || { echo "OpenSSL is not installed. Please install OpenSSL and try again."; exit 1; }; \
		openssl req -new -newkey RSA:2048 -nodes -keyout ssl.key -out ssl.csr -subj '/CN=test.example.com' && \
		openssl genrsa -out rootCA.key 2048 && \
		openssl req -x509 -new -nodes -key rootCA.key -sha256 -days 3650 -out rootCA.pem -subj /CN=TestCA && \
		openssl x509 -req -in ssl.csr -CAcreateserial -out server.crt -sha256 -CAkey rootCA.key -CA rootCA.pem
	@echo "SSL certificate generated successfully."

deploy:      ## Deploy Serverless app to local environment with SSL setup for Route53
	@echo "Generating and importing test SSL certificate to ACM for Route53 domain test.example.com"
	@make cert
	@echo "Importing local test certificate into ACM API ..."
	@awslocal acm import-certificate --certificate fileb://sslcert/server.crt --private-key fileb://sslcert/ssl.key
	@echo "Creating Route53 hosted zone for test domain 'test.example.com' ..."
	@awslocal route53 create-hosted-zone --name test.example.com --caller-reference r1
	@echo "Deploying Serverless app to local environment"
	@SLS_DEBUG=1 npm run deploy
	@echo "Serverless app successfully deployed."

run:         ## Run the app locally and show test invocations
	./run.sh

test:        ## Run tests
	make deploy run target=ci

start:       ## Start LocalStack
	ACTIVATE_PRO=1 localstack start -d

stop:        ## Stop LocalStack
	@echo
	localstack stop

ready:       ## Wait until LocalStack is ready
	@echo Waiting on the LocalStack container...
	@localstack wait -t 30 && echo Localstack is ready to use! || (echo Gave up waiting on LocalStack, exiting. && exit 1)

logs:        ## Retrieve LocalStack logs
	@localstack logs > logs.txt

test-ci:     ## Run CI tests
	make check start install ready test; return_code=`echo $$?`;\
	make logs; make stop; exit $$return_code;

.PHONY: usage check install run cert start stop ready logs test-ci
