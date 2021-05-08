export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION ?= us-east-1
export SERVICES ?= serverless,acm,route53

usage:       ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:     ## Install dependencies
	@npm install
	@which serverless || npm install -g serverless
	@which localstack || pip install localstack
	@which awslocal || pip install awscli-local

cert:        ## Create test SSL certificate
	mkdir -p sslcert
	cd sslcert; \
		which openssl || exit; \
		openssl req -new -newkey RSA:2048 -nodes -keyout ssl.key -out ssl.csr -subj '/CN=test.example.com'; \
		openssl genrsa -out rootCA.key 2048; \
		openssl req -x509 -new -nodes -key rootCA.key -sha256 -days 3650 -out rootCA.pem -subj /CN=TestCA; \
		openssl x509 -req -in ssl.csr -CAcreateserial -out server.crt -sha256 -CAkey rootCA.key -CA rootCA.pem

run:         ## Deploy the app locally and run an API GW test invocation
	@make install; \
		echo "Generating and importing test SSL certificate to ACM for Route53 domain test.example.com"; \
		make cert; \
		echo "Importing local test certificate into ACM API ..."; \
		awslocal acm import-certificate --certificate file://sslcert/server.crt --private-key file://sslcert/ssl.key && \
		echo "Creating Route53 hosted zone for test domain 'test.example.com' ..."; \
		awslocal route53 create-hosted-zone --name test.example.com --caller-reference r1 && \
		echo "Deploying Serverless app to local environment"; \
		SLS_DEBUG=1 npm run deploy && \
		echo "Serverless app successfully deployed. Now trying to invoke the API Gateway endpoints with custom domains." && \
		echo && echo "Invoking endpoint 1: http://test.example.com:4566/hello" && \
		curl -H 'Host: test.example.com' http://localhost:4566/hello && \
		echo && echo && echo "Invoking endpoint 2: http://test.example.com:4566/goodbye" && \
		curl -H 'Host: test.example.com' http://localhost:4566/goodbye

test-ci:
	make install && make run || true

.PHONY: usage install run cert
