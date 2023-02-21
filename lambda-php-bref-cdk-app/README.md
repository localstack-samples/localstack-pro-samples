# LocalStack Demo: Deploying PHP/Bref Lambda via CDK

Simple [PHP/Bref](https://bref.sh/) serverless application using a shared Lambda layer deployable with AWS CDK to LocalStack.

This PHP/Bref application **without fpm** implements a [typed PHP Lambda handler](https://bref.sh/docs/function/handlers.html) as an *HTTP handler class* for serving [API Gateway HTTP events](https://bref.sh/docs/function/handlers.html#api-gateway-http-events).
Bref turns an API Gateway event into a [PSR-7](https://www.php-fig.org/psr/psr-7/)request and one Lambda per route implements a handler class and returns a PSR-7 response.

## PHP/Bref with fpm and Serverless

Bref typically runs [Web applications on AWS Lambda](https://bref.sh/docs/runtimes/http.html) to support traditional PHP frameworks such as Laravel and Symphony.
In this `php-fpm` approach, Bref turns an API Gateway event into a FastCGI (PHP-FPM) request and one Lambda receives all URLs and responds using `echo`, `header()` function, etc.
Checkout the different kinds of applications at [php-runtime/bref](https://github.com/php-runtime/bref) and select the correct layer with or without `fpm` accordingly.

To deploy the `php-fpm` Laravel [base](https://github.com/brefphp/examples/tree/master/Laravel/base) project from [brefphp/examples](https://github.com/brefphp/examples) to LocalStack:

1. Install the [serverless-localstack](https://github.com/LocalStack/serverless-localstack) plugin

    ```bash
    npm install --save-dev serverless-localstack
    ```

2. Add serverless-localstack to `plugins` in the [serverless.yml](https://github.com/brefphp/examples/blob/master/Laravel/base/serverless.yml)

    ```yml
    plugins:
    - ./vendor/bref/bref
    - serverless-localstack
    ```

3. Add `custom` properties in the `serverless.yml`

    ```yml
    custom:
      localstack:
        # list of stages for which the plugin should be enabled
        stages:
          - local
    ```

4. Deploy to LocalStack

    ```bash
    serverless deploy --stage local
    ```

Start localstack with:

* `LAMBDA_DOCKER_FLAGS=--user nobody` until [this user permission issue](https://github.com/localstack/localstack/issues/7722) is resolved for running `fpm`.
* `PROVIDER_OVERRIDE_LAMBDA=v2` until the [new Lambda provider implementation](https://github.com/localstack/localstack/pull/6724) becomes the default in LocalStack Version 2.

## Prerequisites

* LocalStack
* Docker
* `make`
* `curl`
* `jq`
* Node.js / `npm`
* [`cdklocal`](https://github.com/localstack/aws-cdk-local)

## Installing

To install the dependencies:
```
make install
```

## Starting LocalStack

Make sure that LocalStack is started:
```
LOCALSTACK_API_KEY=... PROVIDER_OVERRIDE_LAMBDA=v2 LAMBDA_DOCKER_FLAGS="--user nobody" DEBUG=1 localstack start
```

## Running

Deploy the app locally and run an HTTP test invocation:
```bash
make run
```

The script first bootstraps and deploys the CDK app locally and subsequently invokes the HTTP endpoint via curl (`make invoke`).

```
Outputs:
CdkBrefStack.Url = https://bd0f6b19.execute-api.localhost.localstack.cloud:4566/
Stack ARN:
arn:aws:cloudformation:us-east-1:000000000000:stack/CdkBrefStack/dec480c5

✨  Total time: 7.9s


CDK app successfully deployed. Now trying to invoke the Lambda through API gateway.
endpoint=$(jq .CdkBrefStack.Url cdk-outputs.json --raw-output) && \
	echo endpoint=${endpoint} && \
	curl ${endpoint}?name=LocalStack!
endpoint=https://bd0f6b19.execute-api.localhost.localstack.cloud:4566/
Hello LocalStack!%
```

## License

This code is available under the Apache 2.0 license.
