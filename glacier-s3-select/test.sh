#!/bin/bash

echo "Creating S3 bucket and Glacier vault in LocalStack"
lstk aws s3 mb s3://test1
lstk aws s3 cp data.csv s3://test1/data.csv
echo "Running S3 Select query against CSV file in bucket"
lstk aws s3api select-object-content --bucket test1 --key data.csv \
  --expression 'select count(*), sum(Cost) from s3object' --expression-type SQL \
  --input-serialization 'CSV={FileHeaderInfo=USE}' --output-serialization 'CSV={}' s3-result.csv

echo 'Query results for S3 Select query below'
echo '----'
cat s3-result.csv
echo
echo '----'

echo
echo 'Creating new vault in local Glacier API'
lstk aws glacier create-vault --account-id - --vault-name vault1
lstk aws s3 mb s3://glacier-results
echo 'Uploading test CSV file to new Glacier vault'
archiveId=$(lstk aws glacier upload-archive --vault-name vault1 --account-id - --body data.csv | jq -r '.archiveId')

echo 'Initiating new "select" job in Glacier to query data from CSV file in vault archive'
#sed -i 's/"ArchiveId": ".*"/"ArchiveId": "'$archiveId'"/' glacier-params.json
perl -i -pe 's/"ArchiveId": ".*"/"ArchiveId": "'$archiveId'"/' glacier-params.json
outPath=$(lstk aws glacier initiate-job --account-id - --vault-name vault1 --job-parameters file://glacier-params.json | jq -r '.jobOutputPath')

echo 'Sleep some time to wait for Glacier job to finish'
sleep 3
echo
echo 'Contents of result bucket after running Glacier query:'
lstk aws s3 ls s3://glacier-results/$outPath/results/

echo
echo 'Downloading test CSV file from new Glacier vault'
resultFile=$(lstk aws s3 ls s3://glacier-results/$outPath/results/ | awk '{print $4}')
lstk aws s3 cp s3://glacier-results/$outPath/results/$resultFile glacier-result.csv

echo 'Query results for S3 Select query below'
echo '----'
cat glacier-result.csv
echo
echo '----'
