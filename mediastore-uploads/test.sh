#!/bin/bash

CONTAINER=my-container1

echo "Creating MediaStore container in LocalStack ..."
endpoint=$(awslocal mediastore create-container --container-name $CONTAINER | jq -r '.Container.Endpoint')
echo "MediaStore container endpoint: $endpoint"

echo "Uploading file to MediaStore container ..."
echo 'test file content 123' > /tmp/test-mediastore-file.txt
awslocal mediastore-data --endpoint-url $endpoint put-object --path /test/file.txt --body /tmp/test-mediastore-file.txt

echo "Downloading file from MediaStore container ..."
awslocal mediastore-data --endpoint-url $endpoint get-object --path /test/file.txt /tmp/test-mediastore-file-1.txt
echo "Checking file content of downloaded file ..."
cat /tmp/test-mediastore-file-1.txt | grep 'file content'

echo "Cleaning up - deleting MediaStore container"
awslocal mediastore-data --endpoint-url $endpoint delete-object --path /test/file.txt
awslocal mediastore delete-container --container-name $CONTAINER
