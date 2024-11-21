# LocalStack Demo: Enable Lambda Debug Mode to Automatically Raise Execution Timeouts

A simple demo application showcasing how to debug Java Lambdas locally with Lambda Debug Mode.
The demo deploys a Lambda function with a one-second timeout, which is automatically lifted when running LocalStack with Lambda Debug Mode enabled.

## Prerequisites

* LocalStack
* Docker
* `make`
* [`awslocal`](https://github.com/localstack/awscli-local)
* `java17` and `gradle` (optional for local build)

## Installing

To build the Lambda function archive:

```sh
make install
```

## Starting Up

Make sure that LocalStack is started with the following configuration:

```sh
LOCALSTACK_LAMBDA_DEBUG_MODE=1 \
LOCALSTACK_LAMBDA_DEBUG_MODE_CONFIG_PATH=/tmp/lambda_debug_mode_config.yaml \
localstack start --volume $PWD/lambda_debug_mode_config.yaml:/tmp/lambda_debug_mode_config.yaml
```

* `LOCALSTACK_LAMBDA_DEBUG_MODE=1` enables the Lambda debug mode
* `LOCALSTACK_LAMBDA_DEBUG_MODE_CONFIG_PATH=/tmp/lambda_debug_mode_config.yaml` points to the config file for Lambda debug mode allowing for advanced configuration. It maps the Lambda function `arn:aws:lambda:us-east-1:000000000000:function:function-one` to port `5050`.
* `--volume $PWD/lambda_debug_mode_config.yaml:/tmp/lambda_debug_mode_config.yaml` maps the Lambda debug configuration from the host into the LocalStack Docker container for hot-reloading.

## Running the Sample

The project requires you to configure your IDE or editor of choice to debug remote Java Lambda functions on port 5050.
[These documentations](https://docs.localstack.cloud/user-guide/lambda-tools/debugging/#debugging-jvm-lambdas) include a guide on how you can do so.

The following command used to deploy and invoke the Lambda locally:

```sh
make run
```

### Attaching the Remote Debugger

After the Lambda function is invoked you can switch to your IDE or editor of choice, set a breakpoint in the Lambda handler, and run the remote debugger.
LocalStack will automatically waive the set one second timeout for the Lambda function, giving you ample time to connect the debugger and debug the logic in the function.

## License

The code in this sample is available under the Apache 2.0 license.
