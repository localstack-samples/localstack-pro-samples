# LocalStack Demo: EC2 instances with Docker backend

This examples demos LocalStack EC2 and SSM functionalities when using the Docker backend.

## Prerequisites

* LocalStack
* Docker
* `make`
* [`jq`](https://stedolan.github.io/jq/)

Note: This demo involves the download of the Ubuntu Docker image weighing about 100MB

## Installing

To install the dependencies:
```
make install
```

## Running

Run LocalStack with following enviroment flags:
```
LOCALSTACK_API_KEY=... EC2_VM_MANAGER=docker DEBUG=1 localstack start
```

Run the demo:
```
make run
```

You will see various operations being performed in the logs, starting with
- the creation of a Docker-backed EC2 instance
- command being sent to this instance through SSM
- retrieval standard output of this command
- snapshoting the running instance into a new AMI
- termination of the instance

## License

This code is available under the Apache 2.0 license.
