export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export SERVICES = cloudformation,ecs,ec2
export AWS_DEFAULT_REGION = us-east-1

usage:      ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:    ## Install dependencies
	@which localstack || pip install localstack
	@which packer || (echo 'Please install "packer" (https://www.packer.io) to run this sample'; exit 1)

run:        ## Run packer and build the image locally
	@make install; \
		echo "Starting script to build EC2 image via packer"; \
		./run.sh

test-ci:
	# skip running this test in CI for now

.PHONY: usage install start run
