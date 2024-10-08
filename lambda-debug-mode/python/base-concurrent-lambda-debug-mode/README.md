# LocalStack Demo: Lambda Debug Mode Automatically Handle Concurrent Function Invocations

A simple demo application showcasing how to Lambda Debug Mode automatically controls concurrent lambda call invocations.
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
```
make install
```

## Starting Up

Make sure that LocalStack is started with the following configuration:
```
LAMBDA_DEBUG_MODE=1 \
LAMBDA_DEBUG_MODE_CONFIG_PATH=path/to/lambda_debug_mode_config.yaml \
localstack start
```

Lambda Debug Mode is enabled through the config option `LAMBDA_DEBUG_MODE=1`.

The config option `LAMBDA_DEBUG_MODE_CONFIG_PATH` should point to the provided `yaml` config file for Lambda Debug Mode `lambda_debug_mode_config.yaml`.
The config file contains instructions for Lambda Debug Mode to debug the Lambda function `arn:aws:lambda:us-east-1:000000000000:function:function-one` on port `19891`.


## Running the Sample

The project ships with a Visual Studio Code debug launch config (see `.vscode/launch.json`). This configuration can be used to attach to the code in the Lambda function while it is executing.

The following command used to deploy and invoke the Lambda locally:

```
make run
```

### Attaching the VSCode Debugger

After the Lambda function is invoked you can switch to Visual Studio Code, set a breakpoint in the Lambda handler, and run the preconfigured remote debugger.
LocalStack will automatically waive the set one second timeout for the Lambda function, giving you ample time to connect the debugger and debug the logic in the function.
You should also notice how the debugger connects to the first invocation (the message object would end with `Attempt 1`), whilst the following invocations
are refused automatically by Lambda Debug Mode as explained in the corresponding log messages.

## License

The code in this sample is available under the Apache 2.0 license.

