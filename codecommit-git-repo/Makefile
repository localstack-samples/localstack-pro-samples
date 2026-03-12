export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION=us-east-1
export REPO_FOLDER = /tmp/test.codecommit.repo1

usage:       ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

check:    ## Check if all required prerequisites are installed
	@command -v docker > /dev/null 2>&1 || { echo "Docker is not installed. Please install Docker and try again."; exit 1; }
	@command -v git > /dev/null 2>&1 || { echo "Git is not installed. Please install Git and try again."; exit 1; }
	@command -v localstack > /dev/null 2>&1 || { echo "LocalStack CLI is not installed. Please install it and try again."; exit 1; }
	@command -v awslocal > /dev/null 2>&1 || { echo "awslocal is not installed. Please run: pip install awscli-local"; exit 1; }
	@echo "All required prerequisites are available."


install:     ## Install dependencies
	@which localstack || pip install localstack
	@which awslocal || pip install awscli-local

run:         ## Deploy and run the sample locally
	@echo "-----\nStep 1: Creating new CodeCommit git repository"; \
		awslocal codecommit create-repository --repository-name repo1; \
		gitUrl=$$(awslocal codecommit get-repository --repository-name repo1 | \
			jq -r .repositoryMetadata.cloneUrlSsh); \
		echo "-----\nStep 2: Cloning repo to temporary folder"; \
		test -e $(REPO_FOLDER) || git clone $$gitUrl $(REPO_FOLDER); \
		echo 'test file content 123' >> $(REPO_FOLDER)/test.txt; \
		echo "-----\nStep 3: Committing and pushing new file to the repository"; \
		(cd $(REPO_FOLDER) && git add test.txt && git commit -m test_commit && git push); \
		echo "-----\nStep 4: Cloning repo to second temporary folder"; \
		test -e $(REPO_FOLDER).copy || git clone $$gitUrl $(REPO_FOLDER).copy; \
		echo "-----\nStep 5: Printing file content from second clone of repo"; \
		cat $(REPO_FOLDER).copy/test.txt


start:
	@test -n "${LOCALSTACK_AUTH_TOKEN}" || (echo "LOCALSTACK_AUTH_TOKEN is not set. Find your token at https://app.localstack.cloud/workspace/auth-token"; exit 1)
	DEBUG=1 LOCALSTACK_AUTH_TOKEN=$(LOCALSTACK_AUTH_TOKEN) localstack start -d

stop:
	@echo
	localstack stop
ready:
	@echo Waiting on the LocalStack container...
	@localstack wait -t 30 && echo Localstack is ready to use! || (echo Gave up waiting on LocalStack, exiting. && exit 1)

logs:
	@localstack logs > logs.txt

test-ci:
	make start install ready run; return_code=`echo $$?`;\
	make logs; make stop; exit $$return_code;
		
.PHONY: usage install start run stop ready logs test-ci

