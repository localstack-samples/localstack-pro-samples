# API Gateway with Custom Domains

| Key          | Value                             |
| ------------ | --------------------------------- |
| Environment  | LocalStack                        |
| Services     | API Gateway, Lambda, Route53, ACM |
| Integrations | Serverless Framework              |
| Categories   | Serverless; REST API              |

## Introduction

A demo application showcasing API Gateway (v2) endpoints with custom domain names configured through Route53 and ACM, deployed locally using LocalStack and the Serverless framework. For more details, refer to the [documentation](https://docs.localstack.cloud/user-guide/aws/apigateway/#custom-domain-names-with-api-gateway).

Under the hood, the Serverless framework uses the [`serverless-localstack`](https://github.com/localstack/serverless-localstack) plugin to deploy the application to LocalStack. The plugin is configured in the `serverless.yml` file to use the LocalStack endpoint and the custom domain name.

## Prerequisites

* [Node.js 18.x](https://nodejs.org/en/download/package-manager) with `npm`
* [Serverless Framework](https://www.serverless.com/framework/docs/getting-started) 3.x
* `openssl`

## Check prerequisites

```bash
make check
```

## Installation

```bash
make install
```

## Start LocalStack

```bash
make start
```

## Deploy the Application

```bash
make deploy
```

The script:

-   Generates an SSL certificate for local testing using `openssl`.
-   Uses a predefined certificate if `openssl` is unavailable.
-   Adds the certificate to Amazon Certificate Manager (ACM).
-   Creates a Route53 hosted zone for `test.example.com`.
-   Displays deployment logs of the Serverless application in the output section.
-   Showcases API Gateway endpoints and custom domain configuration.

## Run the application

```bash
make run
```

## License

This code is available under the Apache 2.0 license.
