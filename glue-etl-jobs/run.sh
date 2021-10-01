#!/bin/bash

BUCKET=glue-pyspark-test
JOB_NAME=test-job1
S3_URL=s3://$BUCKET/job.py

echo Putting PySpark script to test S3 bucket ...
awslocal s3 mb s3://$BUCKET
awslocal s3 cp job.py $S3_URL

db_port=$(awslocal rds create-db-cluster --db-cluster-identifier c1 --engine aurora-postgresql --database-name test | jq -r .DBCluster.Port)
echo Using local RDS database on port $db_port ...

echo Creating Glue databases and tables ...
awslocal glue create-database --database-input '{"Name":"legislators"}'
awslocal glue create-table --database legislators \
  --table-input '{"Name":"persons_json", "Parameters": {"connectionName": "c1"}, "StorageDescriptor": {"Location": "test.persons"}}'
awslocal glue create-connection \
  --connection-input '{"Name":"c1", "ConnectionType": "JDBC", "ConnectionProperties": {"USERNAME": "test", "PASSWORD": "test", "JDBC_CONNECTION_URL": "jdbc:postgresql://localhost.localstack.cloud:'$db_port'"}}'

echo Starting Glue job from PySpark script ...
awslocal glue create-job --name $JOB_NAME --role r1 \
  --command '{"Name": "pythonshell", "ScriptLocation": "'$S3_URL'"}' \
  --connections '{"Connections": ["c1"]}'
run_id=$(awslocal glue start-job-run --job-name $JOB_NAME | jq -r .JobRunId)

state=$(awslocal glue get-job-run --job-name $JOB_NAME --run-id $run_id | jq -r .JobRun.JobRunState)
while [ "$state" != SUCCEEDED ]; do
  echo "Waiting for Glue job ID '$run_id' to finish (current status: $state) ..."
  sleep 4
  state=$(awslocal glue get-job-run --job-name $JOB_NAME --run-id $run_id | jq -r .JobRun.JobRunState)
done

echo "Done - Glue job execution finished. Please check the LocalStack container logs for more details."
