#!/bin/bash

APPSYNC_URL=http://localhost:4566/graphql

echo "Deploying Serverless app to local environment"; \
SLS_DEBUG=1 npm run deploy && \
echo "Serverless app successfully deployed." && \
api_id=$(awslocal appsync list-graphql-apis | jq -r '(.graphqlApis[] | select(.name=="test-api")).apiId') && \
echo "DEBUG: api_id is: $api_id" && \
api_key=$(awslocal appsync create-api-key --api-id $api_id | jq -r .apiKey.id) && \
echo "DEBUG: api_key is: $api_key" && \
# echo "Starting a WebSocket client to subscribe to GraphQL mutation operations." && \
# source .venv/bin/activate && \
# (python websocket_client.py "$api_id" &) && sleep 2 && \
echo "Now trying to invoke the AppSync API for DynamoDB integration under $APPSYNC_URL/$api_id." && \
curl -H "Content-Type: application/json" -H "x-api-key: $api_key" -d '{"query":"mutation {addPostDDB(id: \"id-123\"){id}}"}' $APPSYNC_URL/$api_id && \
curl -H "Content-Type: application/json" -H "x-api-key: $api_key" -d '{"query":"mutation {addPostDDB(id: \"id-abc\"){id}}"}' $APPSYNC_URL/$api_id && \
curl -H "Content-Type: application/json" -H "x-api-key: $api_key" -d '{"query":"query {getPostsDDB{id}}"}' $APPSYNC_URL/$api_id

echo -e "\n"
echo "************************************************"
echo "* Logs for data returned from \$context.result  *"
echo "************************************************"
docker logs $(docker ps -q --filter name=localstack-pro-samples_devcontainer-localstack-1) | tail -n 2 | head -n 1
