# Lambda Remote Debugging (Python)

| Key          | Value                                                   |
| ------------ | ------------------------------------------------------- |
| Services     | Lambda                                                  |
| Integrations | AWS SAM, VS Code, AWS Toolkit for VS Code               |
| Categories   | Serverless; Debugging                                   |

## Introduction

A Hello World Python Lambda function demonstrating interactive breakpoint debugging using LocalStack [Lambda Remote Debugging](https://docs.localstack.cloud/aws/tooling/lambda-tools/remote-debugging/). LocalStack automatically configures debugging and adjusts relevant timeouts. The recommended setup uses the AWS Toolkit for VS Code for one-click debugging.

## Prerequisites

- A valid [LocalStack for AWS license](https://localstack.cloud/pricing). Your license provides a [`LOCALSTACK_AUTH_TOKEN`](https://docs.localstack.cloud/getting-started/auth-token/) to activate LocalStack.
- [Docker](https://docs.docker.com/get-docker/)
- [VS Code](https://code.visualstudio.com/) with the [LocalStack Toolkit](https://marketplace.visualstudio.com/items?itemName=localstack.localstack) ≥ 1.2 and [AWS Toolkit](https://marketplace.visualstudio.com/items?itemName=AmazonWebServices.aws-toolkit-vscode) ≥ 3.74
- [Python 3](https://www.python.org/downloads/)
- [AWS CLI v2](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) or [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)

## Check prerequisites

```bash
make check
```

## Installation

```bash
make install
```

## Start LocalStack

1. Execute the VS Code command "LocalStack: Run Setup Wizard" using the LocalStack Toolkit
2. Start LocalStack by clicking on the LocalStack Toolkit status bar

## Deploy the Lambda function

1. Run `make build`
2. Run `make deploy`

## Debug the Lambda function

1. Open the **Remote invoke configuration** in the AWS Toolkit
    1. Open the AWS Toolkit extension
    2. Expand the AWS Explorer and Lambda node
    3. Navigate to the function you want to debug, then choose the Invoke remotely icon ▶️ from the context menu
2. Select the **Remote debugging** check box to display the remote debugging properties
3. Specify the Local Root Path to your local handler file.
4. Set a breakpoint in your handler file by clicking in the gutter-margin
5. Click the **Remote invoke** button to invoke the Lambda function

## Lambda Debug Mode

### Starting Up

1. Start LocalStack with the following configuration:

    ```sh
    LOCALSTACK_AUTH_TOKEN=<your-auth-token> \
    LOCALSTACK_LAMBDA_DEBUG_MODE=1 \
    LOCALSTACK_LAMBDA_DEBUG_MODE_CONFIG_PATH=/tmp/lambda_debug_mode_config.yaml \
    localstack start --volume $PWD/lambda_debug_mode_config.yaml:/tmp/lambda_debug_mode_config.yaml
    ```

    * `LOCALSTACK_AUTH_TOKEN=<your-auth-token>` is the authentication token for LocalStack
    * `LOCALSTACK_LAMBDA_DEBUG_MODE=1` adjusts timeouts
    * `LOCALSTACK_LAMBDA_DEBUG_MODE_CONFIG_PATH=/tmp/lambda_debug_mode_config.yaml` points to the config file for Lambda debug mode allowing for advanced configuration. It maps the Lambda function `arn:aws:lambda:us-east-1:000000000000:function:HelloWorldFunctionPython` to port `8050`.
    * `--volume $PWD/lambda_debug_mode_config.yaml:/tmp/lambda_debug_mode_config.yaml` maps the Lambda debug configuration from the host into the LocalStack Docker container for hot-reloading configuration updates.

### Deploy the Lambda function

1. Run `make build` to build the Lambda ZIP package
2. Run `make deploy` to deploy the Lambda function

### Debug the Lambda function

1. Open the sample folder in VS Code to auto-detect `.vscode/launch.json`
2. Set a breakpoint in the handler file `hello_world/app.py` by clicking in the gutter-margin
3. Open the **Run and Debug** view in VS Code
4. Run the **Python: Remote Attach** task
5. Run `make invoke` to invoke the Lambda function

## Troubleshooting

* Concurrent invokes are currently rejected with a `ResourceConflictException`.
Upvote [this GitHub issue](https://github.com/localstack/localstack/issues/8522) if this affects you.

## License

The code in this sample is available under the Apache 2.0 license.
