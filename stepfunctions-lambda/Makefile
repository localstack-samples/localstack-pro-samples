export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION=us-east-1

usage:       ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

check:    ## Check if all required prerequisites are installed
	@command -v docker > /dev/null 2>&1 || { echo "Docker is not installed. Please install Docker and try again."; exit 1; }
	@command -v python3 > /dev/null 2>&1 || { echo "Python 3 is not installed. Please install Python 3 and try again."; exit 1; }
	@command -v lstk > /dev/null 2>&1 || { echo "lstk CLI is not installed. Please run: npm install -g @localstack/lstk"; exit 1; }
	@command -v aws > /dev/null 2>&1 || { echo "AWS CLI is not installed (required by 'lstk aws'). Please install it and try again."; exit 1; }
	@echo "All required prerequisites are available."


install:     ## Install dependencies

create-lambdas:         ## Create the Lambdas
	lstk aws iam create-role --role-name step-function-lambda --assume-role-policy-document file://step-trust-policy.json
	lstk aws iam attach-role-policy --role-name step-function-lambda --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaRole

	cp -f lambda_adam.py lambda_function.py
	zip package.zip lambda_function.py

	lstk aws lambda create-function \
  		--function-name adam \
  		--role arn:aws:iam::000000000000:role/lambda-demo \
  		--runtime python3.9 --timeout 10 --memory-size 128 \
  		--handler lambda_function.lambda_handler \
  		--zip-file fileb://package.zip
	
	rm package.zip lambda_function.py

	cp -f lambda_cole.py lambda_function.py
	zip package.zip lambda_function.py

	lstk aws lambda create-function \
  		--function-name cole \
  		--role arn:aws:iam::000000000000:role/lambda-demo \
  		--runtime python3.9 --timeout 10 --memory-size 128 \
  		--handler lambda_function.lambda_handler \
  		--zip-file fileb://package.zip

	rm package.zip lambda_function.py

	cp -f lambda_combine.py lambda_function.py
	zip package.zip lambda_function.py

	lstk aws lambda create-function \
  		--function-name combine \
  		--role arn:aws:iam::000000000000:role/lambda-demo \
  		--runtime python3.9 --timeout 10 --memory-size 128 \
  		--handler lambda_function.lambda_handler \
  		--zip-file fileb://package.zip

	rm package.zip lambda_function.py

start:
	@test -n "${LOCALSTACK_AUTH_TOKEN}" || (echo "LOCALSTACK_AUTH_TOKEN is not set. Find your token at https://app.localstack.cloud/workspace/auth-token"; exit 1)
	lstk start --non-interactive --type aws
stop:
	@echo
	lstk stop

ready:
	@echo Waiting on the LocalStack container...
	@lstk status > /dev/null && echo Localstack is ready to use! || (echo Gave up waiting on LocalStack, exiting. && exit 1)

logs:
	@lstk logs > logs.txt

test-ci:
	make start install ready create-lambdas; return_code=`echo $$?`;\
	make logs; make stop; exit $$return_code;
	
.PHONY: usage install create-lambdas run stop ready logs test-ci
