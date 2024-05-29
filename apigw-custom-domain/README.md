# API Gateway with Custom Domains

[![Makefile CI](https://github.com/localstack-samples/localstack-pro-samples/actions/workflows/makefile.yml/badge.svg)](https://github.com/localstack-samples/localstack-pro-samples/actions/workflows/makefile.yml)

| Key          | Value                             |
| ------------ | --------------------------------- |
| Environment  | LocalStack                        |
| Services     | API Gateway, Lambda, Route53, ACM |
| Integrations | Serverless Framework              |
| Categories   | Serverless; REST API              |
| Level        | Beginner                          |

## Introduction

A demo application showcasing API Gateway (v2) endpoints with custom domain names configured through Route53 and ACM, deployed locally using LocalStack and the Serverless framework. For more details, refer to the [documentation](https://docs.localstack.cloud/user-guide/aws/apigateway/#custom-domain-names-with-api-gateway).

## Prerequisites

* [`localstack` CLI](https://docs.localstack.cloud/getting-started/installation/#localstack-cli) with [`LOCALSTACK_AUTH_TOKEN`](https://docs.localstack.cloud/getting-started/auth-token/)
* [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) with [`awslocal` wrapper script](https://docs.localstack.cloud/user-guide/integrations/aws-cli/#localstack-aws-cli-awslocal)
* [Node.js 18.x](https://nodejs.org/en/download/package-manager) with `npm`
* [Serverless Framework](https://www.serverless.com/framework/docs/getting-started) 3.x
* Docker
* `openssl` & `make`

You can run `make check` to verify that all dependencies are installed.

## Installation

Run the following command to install the necessary dependencies:

```bash
make install
```

## Start LocalStack

To start LocalStack, run the following command:

```bash
LOCALSTACK_AUTH_TOKEN=... DEBUG=1 localstack start
```

## Deploy the Application

Deploy the application locally using the Serverless framework:

```
./run.sh
```

The script initially generates an SSL certificate for local testing. If the `openssl` command is unavailable, it uses an existing predefined certificate. The script then adds the certificate to Amazon Certificate Manager (ACM) and creates a Route53 hosted zone for the domain name `test.example.com`.

Next, you will see the deployment logs of the Serverless application, with details displayed in the output section towards the bottom. The script then showcases the API Gateway endpoints and the custom domain name configuration, along with sample commands to invoke the deployed endpoints.

```bash
Serverless app successfully deployed.
Now trying to invoke the API Gateway endpoints with custom domains.
Sample command to invoke endpoint 1:
curl -H 'Host: test.example.com' http://localhost:4566/hello
Sample command to invoke endpoint 2:
curl -H 'Host: test.example.com' http://localhost:4566/goodbye
```

Under the hood, the Serverless framework uses the [`serverless-localstack`](https://github.com/localstack/serverless-localstack) plugin to deploy the application to LocalStack. The plugin is configured in the `serverless.yml` file to use the LocalStack endpoint and the custom domain name.

## License

This code is available under the Apache 2.0 license.
