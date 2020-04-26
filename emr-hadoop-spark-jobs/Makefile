export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export SERVICES = serverless
export AWS_DEFAULT_REGION=us-east-1

usage:       ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:     ## Install dependencies
	@which localstack || pip install localstack
	@which awslocal || pip install awscli-local
	@docker images | grep localstack/spark || docker pull localstack/spark

run:         ## Build and deploy the app locally
	@make install
	@echo "Building Java project..."
	(cd job; test -e target/localstack-emr-test-0.1.0-shaded.jar || mvn package)

	@echo "Uploading test files to local S3..."
	awslocal s3 mb s3://bucket1
	awslocal s3 mb s3://bucket2
	awslocal s3 mb s3://bucket3
	awslocal s3 cp job/target/localstack-emr-test-0.1.0-shaded.jar s3://bucket1/test.jar
	@echo '<test1/>' > /tmp/job1.xml.tmp
	awslocal s3 cp /tmp/job1.xml.tmp s3://bucket1/job1.xml
	@echo '<test2/>' > /tmp/job2.xml.tmp
	awslocal s3 cp /tmp/job2.xml.tmp s3://bucket1/job2.xml

	@echo "Creating local EMR cluster and running init jobs (this may take some time)..."
	awslocal emr create-cluster \
    --release-label emr-5.9.0 --applications Name=Spark --ec2-attributes KeyName=myKey \
    --instance-groups InstanceGroupType=MASTER,InstanceCount=1,InstanceType=m4.large InstanceGroupType=CORE,InstanceCount=2,InstanceType=m4.large \
    --steps "`cat steps.json`"

	@echo "The job should have copied file "job1.xml" to bucket bucket2:"
	awslocal s3 ls s3://bucket2/
	@echo "The Spark job should have copied file "job2.xml" to bucket bucket3:"
	awslocal s3 ls s3://bucket3/

test-ci:
	# skip test in CI for now, to avoid downloading large Docker image

.PHONY: usage install run
