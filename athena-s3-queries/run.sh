#!/bin/bash

BUCKET=athena-test
DATABASE=test_db
TABLE=test_table
S3_INPUT=s3://$BUCKET/data/data.csv
S3_OUTPUT=s3://$BUCKET/results

echo Uploading test data to S3...
awslocal s3 mb s3://$BUCKET
awslocal s3 cp data/data.csv $S3_INPUT

echo Running queries to create database and table definitions...
awslocal athena start-query-execution --query-string "`cat queries/create_database.sql`" > /dev/null
awslocal athena start-query-execution --query-string "`cat queries/create_tables.sql`" --query-execution-context Database=$DATABASE --result-configuration OutputLocation=$S3_OUTPUT > /dev/null

queryId=$(awslocal athena start-query-execution --query-string "`cat queries/query_persons.sql`" --query-execution-context Database=$DATABASE --result-configuration OutputLocation=$S3_OUTPUT | jq -r '.QueryExecutionId')
echo Starting SELECT query over data in S3. Query ID: $queryId

outputLoc=$(awslocal athena get-query-execution --query-execution-id $queryId | jq -r '.QueryExecution.ResultConfiguration.OutputLocation')
echo S3 query output location: $outputLoc

awslocal s3 cp $outputLoc/results.csv /tmp/$queryId.results.csv
echo Query result downloaded from S3:
cat /tmp/$queryId.results.csv
