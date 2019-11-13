export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export SERVICES = serverless,appsync
export AWS_DEFAULT_REGION=us-east-1

usage:       ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:     ## Install dependencies
	@test -e node_modules || npm install
	@which serverless || npm install -g serverless
	@which localstack || pip install localstack
	@which awslocal || pip install awscli-local

run:         ## Deploy the app locally and run a Lambda test invocation
	@make install; \
		echo "Deploying Serverless app to local environment"; \
		SLS_DEBUG=1 npm run deploy && \
		echo "Serverless app successfully deployed. Now trying to invoke the AppSync API." && \
		api_id=$$(awslocal appsync list-graphql-apis | jq -r .graphqlApis[0].apiId) && \
		curl -d '{"query":"mutation {addPost(id: \"id123\"){id{S}}}"}' http://localhost:4605/graphql/$$api_id && \
		curl -d '{"query":"query {getPosts{id{S}}}"}' http://localhost:4605/graphql/$$api_id

.PHONY: usage install start lint
