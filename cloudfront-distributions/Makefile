export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION = us-east-1
export SERVICES = serverless,ssm,cloudfront

usage:      ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:    ## Install dependencies
	@which localstack || pip install localstack
	@which awslocal || pip install awscli-local

run:        ## Deploy the app locally and invoke the CloudFront distribution
	@make install; \
		echo "Deploying the app locally"; \
		sls deploy --stage local && \
		api_id=$$(awslocal apigateway get-rest-apis | jq -r '.items[0].id') && \
		awslocal s3 cp html/index.html s3://htmlpages/index.html && \
		sed -i '' 's/"[0-9a-z]*\.execute\-api\./"'$$api_id'.execute-api./g' distconfig.json && \
		cf_domain=$$(awslocal cloudfront create-distribution --distribution-config \
			file://distconfig.json | jq -r '.Distribution.DomainName') && \
		echo "Injecting CloudFront domain $$cf_domain into code and redeploying Lambda" && \
		sed -i '' 's|//.*cloudfront\.net|//'$$cf_domain'|g' handler.js && \
		sls deploy --stage local && \
		echo "Trying to call distribution endpoint (note: it may take a few minutes for the DNS name to become available)" && \
		echo curl -k https://$$cf_domain/index && \
		curl -k https://$$cf_domain/index


.PHONY: usage install start lint
