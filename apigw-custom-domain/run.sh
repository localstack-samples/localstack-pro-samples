#!/bin/bash

function deploy_app() {
  echo "Generating and importing test SSL certificate to ACM for Route53 domain test.example.com"
  make cert

  echo "Importing local test certificate into ACM API ..."
  awslocal acm import-certificate --certificate fileb://sslcert/server.crt --private-key fileb://sslcert/ssl.key

  echo "Creating Route53 hosted zone for test domain 'test.example.com' ..."
  awslocal route53 create-hosted-zone --name test.example.com --caller-reference r1

  echo "Deploying Serverless app to local environment"
  SLS_DEBUG=1 npm run deploy

  echo "Serverless app successfully deployed."
}

function invoke_endpoints() {
  echo "Invoking endpoint 1: http://test.example.com:4566/hello"
  response1=$(curl -H 'Host: test.example.com' http://localhost:4566/hello)
  ../assert "$response1" = "hello world"

  echo "Invoking endpoint 2: http://test.example.com:4566/goodbye"
  response2=$(curl -H 'Host: test.example.com' http://localhost:4566/goodbye)
  ../assert "$response2" = "goodbye"
}

deploy_app

if [[ "$1" == "--ci" ]]; then
  invoke_endpoints
else
  echo "Now trying to invoke the API Gateway endpoints with custom domains."
  echo "Sample command to invoke endpoint 1:"
  echo "curl -H 'Host: test.example.com' http://localhost:4566/hello"
  echo "Sample command to invoke endpoint 2:"
  echo "curl -H 'Host: test.example.com' http://localhost:4566/goodbye"
fi
