# LocalStack Demo: FTP Upload to S3 Bucket via AWS Transfer API

Simple demo application illustrating the use of AWS Transfer API in LocalStack.

## Prerequisites

* LocalStack
* Docker
* `make`

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

The following command runs the test application locally, creates an FTP server via AWS Transfer API locally, uploads two files via FTP, and downloads the files from the target S3 bucket:
```
make run
```

You should then see a couple of log messages in the terminal:
```
Running Test: Creating FTP server and uploading files to S3 via Transfer API
Creating FTP server in AWS Transfer API
Connecting to AWS Transfer FTP server on local port 4510
Uploading file to FTP root directory
Uploading file to FTP sub-directory
Downloading files from S3 root and sub-directory
Test done.
```

## License

This code is available under the Apache 2.0 license.
