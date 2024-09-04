export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION = us-east-1
VENV_DIR ?= .venv

usage:       ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

build-zip:   ## Build the Lambda funzion zip.
	cd java-lambda-function/base-enable-lambda-debug-mode/ && ./gradlew buildZip

run:         ## Deploy and invoke the Lambda container locally
	echo "Deploying Lambda locally"; \
	./run.sh; \
	echo "Done - test successfully finished."

.PHONY: usage install run

