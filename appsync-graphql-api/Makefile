export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export SERVICES = serverless,appsync,dynamodb,rds,secretsmanager
export AWS_DEFAULT_REGION=us-east-1
APPSYNC_URL = http://localhost:4566/graphql

usage:       ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:     ## Install dependencies
	@test -e node_modules || npm install
	@which serverless || npm install -g serverless
	@which localstack || pip install localstack
	@which awslocal || pip install awscli-local
	@test -e .venv || (python3 -m venv .venv; source .venv/bin/activate; pip install -r requirements.txt)

run:         ## Deploy the app locally and run an AppSync GraphQL test invocation
	@make install; \
		echo "Deploying Serverless app to local environment"; \
		SLS_DEBUG=1 npm run deploy && \
		echo "Serverless app successfully deployed." && \
		api_id=$$(awslocal appsync list-graphql-apis | jq -r '(.graphqlApis[] | select(.name=="test-api")).apiId') && \
		echo "DEBUG: api_id is: $$api_id" && \
		api_key=$$(awslocal appsync create-api-key --api-id $$api_id) && \
		echo "DEBUG: api_key is: $$api_key" && \
		echo "Starting a WebSocket client to subscribe to GraphQL mutation operations." && \
		(source .venv/bin/activate; python websocket_client.py "$$api_id" &) && sleep 2 && \
		echo "Now trying to invoke the AppSync API for DynamoDB integration." && \
		curl -H "x-api-key: $$api_key" -d '{"query":"mutation {addPostDDB(id: \"id123\"){id}}"}' $(APPSYNC_URL)/$$api_id && \
		#echo "DEBUG: $$(curl -H "x-api-key: $$api_key" -d '{"query":"mutation {addPostDDB(id: \"id123\"){id}}"}' $(APPSYNC_URL)/$$api_id)" && \
		curl -H "x-api-key: $$api_key" -d '{"query":"query {getPostsDDB{id}}"}' $(APPSYNC_URL)/$$api_id && \
		#echo "DEBUG: $$(curl -H "x-api-key: $$api_key" -d '{"query":"query {getPostsDDB{id}}"}' $(APPSYNC_URL)/$$api_id)" && \
		echo "Scanning items from DynamoDB table - should include entry with 'id123':" && \
		awslocal dynamodb scan --table-name table1 && \
		echo "Now trying to invoke the AppSync API for RDS integration." && \
		curl -H "x-api-key: $$api_key" -d '{"query":"mutation {addPostRDS(id: \"id123\"){id}}"}' $(APPSYNC_URL)/$$api_id && \
		curl -H "x-api-key: $$api_key" -d '{"query":"query {getPostsRDS{id}}"}' $(APPSYNC_URL)/$$api_id

test-ci:
	make install && make run

.PHONY: usage install start lint
