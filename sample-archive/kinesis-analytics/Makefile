export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export SERVICES = serverless,kinesisanalytics
export AWS_DEFAULT_REGION=us-east-1

usage:       ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:     ## Install dependencies
	#@npm install
	@which localstack || pip install localstack
	@which awslocal || pip install awscli-local

deploy:
	@echo "Deploying app to local environment"; \
		awslocal cloudformation create-stack --stack-name test-kinesis --template-body file://analytics.app.cf.yml; \
		echo "Kinesis Analytics stack successfully deployed."; \
		echo "Sleeping some time to wait for the application and Kinesis listeners to start up ..."; \
		for i in {1..7}; do  \
                        sleep 15; \
			status=$$(awslocal kinesisanalytics describe-application --application-name sampleApp \
			| jq -r .ApplicationDetail.ApplicationStatus); \
			echo "Application status: $$status"; if [ "$$status" = "RUNNING" ]; then break; fi;  \
		done; \
		awslocal kinesis list-streams; \
		awslocal kinesisanalytics list-applications

query:
	@outStream=$$(awslocal kinesis list-streams  | jq -r '.StreamNames[]' | grep Output); \
		inStream=$$(awslocal kinesis list-streams  | jq -r '.StreamNames[]' | grep Input); \
		echo "Subscribing to output Kinesis stream $$outStream"; \
		iter=$$(awslocal kinesis get-shard-iterator --stream-name $$outStream \
			--shard-id shardId-000000000000 --shard-iterator-type TRIM_HORIZON | jq -r .ShardIterator); \
		echo "Putting records to input Kinesis stream $$inStream"; \
		awslocal kinesis put-record --stream-name $$inStream \
			--data '{"symbol":"TEST","price":123,"volume":100}' --partition-key test; \
		echo "Waiting for query results... (should print a record array with base64-encoded 'Data' below)"; \
		sleep 10; \
		awslocal kinesis get-records --shard-iterator $$iter | jq .Records

run:         ## Deploy the app and run the streaming queries locally
	@make install
	@make deploy
	@make query

test-ci:
	make install && make run || true

.PHONY: usage install run
