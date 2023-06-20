export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION=us-east-1

usage:       ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:     ## Install dependencies
	@which awslocal || pip install awscli-local

create-lambdas:         ## Create the Lambdas
	awslocal iam create-role --role-name step-function-lambda --assume-role-policy-document file://step-trust-policy.json
	awslocal iam attach-role-policy --role-name step-function-lambda --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaRole

	cp -f lambda_adam.py lambda_function.py
	zip package.zip lambda_function.py

	awslocal lambda create-function \
  		--function-name adam \
  		--role arn:aws:iam::000000000000:role/lambda-demo \
  		--runtime python3.9 --timeout 10 --memory-size 128 \
  		--handler lambda_function.lambda_handler \
  		--zip-file fileb://package.zip
	
	rm package.zip lambda_function.py

	cp -f lambda_cole.py lambda_function.py
	zip package.zip lambda_function.py

	awslocal lambda create-function \
  		--function-name cole \
  		--role arn:aws:iam::000000000000:role/lambda-demo \
  		--runtime python3.9 --timeout 10 --memory-size 128 \
  		--handler lambda_function.lambda_handler \
  		--zip-file fileb://package.zip

	rm package.zip lambda_function.py

	cp -f lambda_combine.py lambda_function.py
	zip package.zip lambda_function.py

	awslocal lambda create-function \
  		--function-name combine \
  		--role arn:aws:iam::000000000000:role/lambda-demo \
  		--runtime python3.9 --timeout 10 --memory-size 128 \
  		--handler lambda_function.lambda_handler \
  		--zip-file fileb://package.zip

	rm package.zip lambda_function.py

start:
	localstack start -d

stop:
	@echo
	localstack stop

ready:
	@echo Waiting on the LocalStack container...
	@localstack wait -t 30 && echo Localstack is ready to use! || (echo Gave up waiting on LocalStack, exiting. && exit 1)

logs:
	@localstack logs > logs.txt

test-ci:
	make start install ready create-lambdas; return_code=`echo $$?`;\
	make logs; make stop; exit $$return_code;
	
.PHONY: usage install create-lambdas run stop ready logs test-ci
