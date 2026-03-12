# PHP/Bref Lambda with CDK

| Key          | Value                               |
| ------------ | ----------------------------------- |
| Services     | Lambda, API Gateway                 |
| Integrations | AWS CDK, Bref, PHP                  |
| Categories   | Serverless; PHP                     |

## Introduction

A [PHP/Bref](https://bref.sh/) serverless application using a shared Lambda layer deployable with AWS CDK to LocalStack. The application implements a typed PHP Lambda handler as an HTTP handler class for serving API Gateway HTTP events. Bref turns API Gateway events into PSR-7 requests for PHP processing.

## Prerequisites

- A valid [LocalStack for AWS license](https://localstack.cloud/pricing). Your license provides a [`LOCALSTACK_AUTH_TOKEN`](https://docs.localstack.cloud/getting-started/auth-token/) to activate LocalStack.
- [Docker](https://docs.docker.com/get-docker/)
- [`localstack` CLI](https://docs.localstack.cloud/getting-started/installation/#localstack-cli)
- [`cdklocal`](https://github.com/localstack/aws-cdk-local) — install with `npm install -g aws-cdk-local`
- [Node.js](https://nodejs.org/en/download/) with `npm`
- [`curl`](https://curl.se/) and [`jq`](https://stedolan.github.io/jq/)

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
export LOCALSTACK_AUTH_TOKEN=<your-auth-token>
make start
```

## Run the application

```bash
make run
```

The script bootstraps and deploys the CDK app locally, then invokes the HTTP endpoint via `curl`. You should see output similar to:

```
Outputs:
CdkBrefStack.Url = https://bd0f6b19.execute-api.localhost.localstack.cloud:4566/
Stack ARN:
arn:aws:cloudformation:us-east-1:000000000000:stack/CdkBrefStack/dec480c5

✨  Total time: 7.9s

CDK app successfully deployed. Now trying to invoke the Lambda through API gateway.
endpoint=https://bd0f6b19.execute-api.localhost.localstack.cloud:4566/
Hello LocalStack!
```

## PHP/Bref with FPM and Serverless Framework

Bref also supports running web applications on AWS Lambda via [php-fpm](https://bref.sh/docs/runtimes/http.html), enabling traditional PHP frameworks like Laravel and Symfony. To deploy a `php-fpm` Laravel project from [brefphp/examples](https://github.com/brefphp/examples) to LocalStack:

1. Install the [serverless-localstack](https://github.com/LocalStack/serverless-localstack) plugin:
   ```bash
   npm install --save-dev serverless-localstack
   ```

2. Add `serverless-localstack` to `plugins` in `serverless.yml`:
   ```yml
   plugins:
     - ./vendor/bref/bref
     - serverless-localstack
   ```

3. Add `custom` properties:
   ```yml
   custom:
     localstack:
       stages:
         - local
   ```

4. Deploy:
   ```bash
   serverless deploy --stage local
   ```

## License

This code is available under the Apache 2.0 license.
