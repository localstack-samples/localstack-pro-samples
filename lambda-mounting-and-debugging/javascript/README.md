# LocalStack Demo: Lambda Code Mounting and Debugging

Simple demo application to illustrate debugging NodeJS Lambdas locally.

## Prerequisites

* LocalStack
* Docker
* `make`
* [`awslocal`](https://github.com/localstack/awscli-local)

## Installation

To install the dependencies:

```sh
make install
```

## Starting Up

You can start LocalStack with Docker Compose:

```sh
docker-compose up -d
```

Alternatively, you can use the following `localstack` CLI configuration:

```sh
LAMBDA_DOCKER_FLAGS='-e NODE_OPTIONS=--inspect-brk=0.0.0.0:9229 -p 9229:9229' \
    LAMBDA_REMOTE_DOCKER=0 \
    localstack start -d
```

## Running the sample

The project ships with a Visual Studio Code debug launch config (see `.vscode/launch.json`). This configuration can be used to attach to the code in the Lambda function while it is executing.

The following command deploys the Lambda and finally invoke the Lambda locally:

```sh
make run
```

# License

The code in this sample is available under the Apache 2.0 license.
