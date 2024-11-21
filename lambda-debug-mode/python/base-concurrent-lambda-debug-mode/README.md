# LocalStack Demo: Lambda Debug Mode Automatically Handle Concurrent Function Invocations

A simple demo application showcasing how Lambda Debug Mode automatically controls concurrent lambda call invocations.
The demo deploys a Lambda function with a one-second timeout, and continues to invoke this function
three times. Upon connecting the remote debugger, the user should see how only the first call is received and can be
debugged, with concurrency error messages being logged about the following two invocations.

## Prerequisites

* LocalStack
* Docker
* `make`
* [`awslocal`](https://github.com/localstack/awscli-local)

## Installing

To install the dependencies:

```sh
make install
```

## Starting Up

```sh
LOCALSTACK_LAMBDA_DEBUG_MODE=1 \
LOCALSTACK_LAMBDA_DEBUG_MODE_CONFIG_PATH=/tmp/lambda_debug_mode_config.yaml \
localstack start --volume $PWD/lambda_debug_mode_config.yaml:/tmp/lambda_debug_mode_config.yaml
```

* `LOCALSTACK_LAMBDA_DEBUG_MODE=1` enables the Lambda debug mode
* `LOCALSTACK_LAMBDA_DEBUG_MODE_CONFIG_PATH=/tmp/lambda_debug_mode_config.yaml` points to the config file for Lambda debug mode allowing for advanced configuration. It maps the Lambda function `arn:aws:lambda:us-east-1:000000000000:function:function-one` to port `19891`.
* `--volume $PWD/lambda_debug_mode_config.yaml:/tmp/lambda_debug_mode_config.yaml` maps the Lambda debug configuration from the host into the LocalStack Docker container for hot-reloading.

## Running the Sample

The project ships with a Visual Studio Code debug launch config (see `.vscode/launch.json`). This configuration can be used to attach to the code in the Lambda function while it is executing.

The following command used to deploy and invoke the Lambda locally:

```sh
make run
```

### Attaching the VSCode Debugger

After the Lambda function is invoked you can switch to Visual Studio Code, set a breakpoint in the Lambda handler, and run the pre-configured remote debugger.
LocalStack will automatically waive the set one second timeout for the Lambda function, giving you ample time to connect the debugger and debug the logic in the function.
You should also notice how the debugger connects to the first invocation (the message object would end with `Attempt 1`), whilst the following invocations
are refused automatically by Lambda Debug Mode as explained in the corresponding log messages.

## License

The code in this sample is available under the Apache 2.0 license.
