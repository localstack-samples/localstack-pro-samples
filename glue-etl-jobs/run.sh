#!/bin/bash

BUCKET=glue-pyspark-test
JOB_NAME=test-job1
S3_URL=s3://$BUCKET/job.py

echo Putting PySpark script to test S3 bucket ...
awslocal s3 mb s3://$BUCKET
awslocal s3 cp job.py $S3_URL
awslocal s3 mb s3://glue-sample-target

awslocal rds create-db-cluster --db-cluster-identifier $cluster_identifier --engine aurora-postgresql --database-name test

cluster_identifier=glue_etl_cluster1

db_port=$(awslocal rds describe-db-clusters --db-cluster-identifier $cluster_identifier | jq -r '.DBClusters[0].Port')
echo Using local RDS database on port $db_port ...

echo Creating Glue databases and tables ...
awslocal glue create-database --database-input '{"Name": "legislators"}'
awslocal glue create-table --database legislators \
  --table-input '{"Name":"memberships_json", "Parameters": {"connectionName": "$cluster_identifier"}, "StorageDescriptor": {"Location": "test.memberships"}}'
awslocal glue create-table --database legislators \
  --table-input '{"Name":"persons_json", "Parameters": {"connectionName": "$cluster_identifier"}, "StorageDescriptor": {"Location": "test.persons"}}'
awslocal glue create-table --database legislators \
  --table-input '{"Name":"organizations_json", "Parameters": {"connectionName": "$cluster_identifier"}, "StorageDescriptor": {"Location": "test.organizations"}}'
awslocal glue create-connection \
  --connection-input '{"Name":"$cluster_identifier", "ConnectionType": "JDBC", "ConnectionProperties": {"USERNAME": "test", "PASSWORD": "test", "JDBC_CONNECTION_URL": "jdbc:postgresql://localhost.localstack.cloud:'$db_port'"}}'

secret=$(awslocal secretsmanager create-secret --name mysecret --secret-string "12345678" | jq -r ".ARN")

echo Creating Postgres database tables with data ...
awslocal rds-data execute-statement --resource-arn arn:aws:rds:us-east-1:000000000000:cluster:$cluster_identifier --secret-arn $secret --sql 'CREATE TABLE IF NOT EXISTS persons(id varchar, name varchar)'
awslocal rds-data execute-statement --resource-arn arn:aws:rds:us-east-1:000000000000:cluster:$cluster_identifier --secret-arn $secret --sql 'CREATE TABLE IF NOT EXISTS organizations(org_id varchar, org_name varchar)'
awslocal rds-data execute-statement --resource-arn arn:aws:rds:us-east-1:000000000000:cluster:$cluster_identifier --secret-arn $secret --sql 'CREATE TABLE IF NOT EXISTS memberships(person_id varchar, organization_id varchar)'
awslocal rds-data execute-statement --resource-arn arn:aws:rds:us-east-1:000000000000:cluster:$cluster_identifier --secret-arn $secret --sql "insert into persons(id, name) VALUES('p1', 'person 1')"
awslocal rds-data execute-statement --resource-arn arn:aws:rds:us-east-1:000000000000:cluster:$cluster_identifier --secret-arn $secret --sql "insert into organizations(org_id, org_name) VALUES('o1', 'org1')"
awslocal rds-data execute-statement --resource-arn arn:aws:rds:us-east-1:000000000000:cluster:$cluster_identifier --secret-arn $secret --sql "insert into memberships(person_id, organization_id) VALUES('p1', 'o1')"
awslocal rds-data execute-statement --resource-arn arn:aws:rds:us-east-1:000000000000:cluster:$cluster_identifier --secret-arn $secret --sql 'CREATE TABLE IF NOT EXISTS hist_root(id varchar, name varchar, org_id varchar, org_name varchar, person_id varchar, organization_id varchar)'

echo Starting Glue job from PySpark script ...
awslocal glue create-job --name $JOB_NAME --role r1 \
  --command '{"Name": "pythonshell", "ScriptLocation": "'$S3_URL'"}' \
  --connections '{"Connections": ["$cluster_identifier"]}'
run_id=$(awslocal glue start-job-run --job-name $JOB_NAME | jq -r .JobRunId)

state=$(awslocal glue get-job-run --job-name $JOB_NAME --run-id $run_id | jq -r .JobRun.JobRunState)
while [ "$state" != SUCCEEDED ]; do
  echo "Waiting for Glue job ID '$run_id' to finish (current status: $state) ..."
  sleep 4
  state=$(awslocal glue get-job-run --job-name $JOB_NAME --run-id $run_id | jq -r .JobRun.JobRunState)
done

echo "Done - Glue job execution finished. Please check the LocalStack container logs for more details."
