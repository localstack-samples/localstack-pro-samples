#!/bin/bash

BUCKET=athena-test
DATABASE=test_db
TABLE=test_table
S3_INPUT=s3://$BUCKET/data/data.csv
S3_OUTPUT=s3://$BUCKET/results

echo Uploading test data to S3...
awslocal s3 mb s3://$BUCKET
awslocal s3 cp data/data.csv $S3_INPUT

function wait_for_query {
  for i in {1..50}; do
    status=$(awslocal athena get-query-execution --query-execution-id $1 | jq -r '.QueryExecution.Status.State')
    echo Waiting for completion status of query $1: $status
    if [ "$status" != "RUNNING" ]; then
      return
    fi
    sleep 6
  done
  echo "Query did not finish in time. There seems to be a problem. Pleaes take a look at the LocalStack logs."
  exit 1
}

echo Running queries to create database and table definitions...
echo 'NOTE: This can take a very long time (several minutes) as the system is initializing'
queryId=$(awslocal athena start-query-execution --query-string "`cat queries/create_database.sql`" | jq -r '.QueryExecutionId')
wait_for_query $queryId
queryId=$(awslocal athena start-query-execution --query-string "`cat queries/create_tables.sql`" --query-execution-context Database=$DATABASE --result-configuration OutputLocation=$S3_OUTPUT | jq -r '.QueryExecutionId')
wait_for_query $queryId

queryId=$(awslocal athena start-query-execution --query-string "`cat queries/query_persons.sql`" --query-execution-context Database=$DATABASE --result-configuration OutputLocation=$S3_OUTPUT | jq -r '.QueryExecutionId')
echo Starting SELECT query over data in S3. Query ID: $queryId

outputLoc=$(awslocal athena get-query-execution --query-execution-id $queryId | jq -r '.QueryExecution.ResultConfiguration.OutputLocation')
echo S3 query output location: $outputLoc
sleep 6

echo 'Waiting for query results to become available in S3 (this can take some time)'
sleep 15
awslocal s3 cp $outputLoc/results.csv /tmp/$queryId.results.csv
echo Query result downloaded from S3:
cat /tmp/$queryId.results.csv
