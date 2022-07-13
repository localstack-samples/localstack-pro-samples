# LocalStack Demo: MediaStore Containers

Simple demo application illustrating the use of the MediaStore API using LocalStack.

## Prerequisites

* LocalStack
* Docker
* `make`
* [`awslocal`](https://github.com/localstack/awscli-local)

## Installing

To install the dependencies:
```
make install
```

## Running

Make sure that LocalStack is started:
```
LOCALSTACK_API_KEY=... DEBUG=1 localstack start
```

The following command runs the example, which creates a MediaStore container, uploads and downloads files to/from the container, and finally cleans up the created resources:
```
make run
```

After the test script completes, the logs in your terminal should look similar to the output below:
```
$ make run
Creating MediaStore container in LocalStack ...
MediaStore container endpoint: http://localhost:4510/my-container1
Uploading file to MediaStore container ...
{
    "ContentSHA256": "",
    "ETag": "\"bf10a48192efd84f35b9a79fb3a18b70\"",
    "StorageClass": ""
}
Downloading file from MediaStore container ...
{
    "ContentLength": "22",
    "ContentType": "",
    "ETag": "\"bf10a48192efd84f35b9a79fb3a18b70\"",
    "StatusCode": 200
}
Checking file content of downloaded file ...
test file content 123
Cleaning up - deleting MediaStore container
```

## License

This code is available under the Apache 2.0 license.
