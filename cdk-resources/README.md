# LocalStack Demo: Deploying Resources via CDK

Simple demo application illustrating deployment of AWS CDK resources locally using LocalStack.

## Prerequisites

* LocalStack
* Docker
* `make`
* [`cdklocal`](https://github.com/localstack/aws-cdk-local)
* [`awslocal`](https://github.com/localstack/awscli-local)

## Installing

To install the dependencies:
```
make install
```

## Starting LocalStack

Make sure that LocalStack is started:
```
LOCALSTACK_API_KEY=... DEBUG=1 localstack start
```

## Running

Bootstrap and deploy the CDK app locally:
```
cdklocal bootstrap
cdklocal deploy
```

More details following soon.

## License

This code is available under the Apache 2.0 license.
