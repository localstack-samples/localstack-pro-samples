# LocalStack Demo: Enable Lambda Debug Mode to Automatically Raise Execution Timeouts

A simple demo application showcasing how to debug Python Lambdas locally with Lambda Debug Mode.
The demo deploys a Lambda function with a one-second timeout, which is automatically lifted when running LocalStack with Lambda Debug Mode enabled.

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

The following command used to first install the dependencies (e.g., `debugpy`), then deploy, and finally invoke the Lambda locally:

```
make run
```

### Attaching the VSCode Debugger

After the Lambda function is invoked you can switch to Visual Studio Code, set a breakpoint in the Lambda handler, and run the preconfigured remote debugger.
LocalStack will automatically waive the set one second timeout for the Lambda function, giving you ample time to connect the debugger and debug the logic in the function.

### Quick Dev Loop with Lambda Code Mounting

Note that, since the Lambda code is mounted from your local filesystem into the Lambda container (by means of `hot-reload` as special bucket name in `run.sh`),
all changes are immediately reflected. For example, you could change the implementation of the handler as follows:
```
def handler(event, context):
    """Lambda handler that will get invoked by the LocalStack runtime"""

    # Wait for the debugger to get attached.
    wait_for_debug_client()

    # Print the incoming invocation event.
    print(event)

    # Additional line added below:
    print("!! Additional log output !!")

    # Return the incomeing invocation evant.
    return event
```
and then upon next invocation of the Lambda, the additional print output will immediately appear in the Lambda logs.
This allows for a quick dev/debug loop, without the need to redeploy the Lambda after the handler is changed!

## License

The code in this sample is available under the Apache 2.0 license.

