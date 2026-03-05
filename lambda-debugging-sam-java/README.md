# Lambda Remote Debugging (Java)

| Key          | Value                                                   |
| ------------ | ------------------------------------------------------- |
| Services     | Lambda                                                  |
| Integrations | AWS SAM, VS Code, AWS Toolkit for VS Code               |
| Categories   | Serverless; Debugging                                   |

## Introduction

A Hello World Java Lambda function demonstrating interactive breakpoint debugging using LocalStack [Lambda Remote Debugging](https://docs.localstack.cloud/aws/tooling/lambda-tools/remote-debugging/). LocalStack automatically configures debugging and adjusts relevant timeouts. The recommended setup uses the AWS Toolkit for VS Code for one-click debugging.

## Prerequisites

- A valid [LocalStack for AWS license](https://localstack.cloud/pricing). Your license provides a [`LOCALSTACK_AUTH_TOKEN`](https://docs.localstack.cloud/getting-started/auth-token/) to activate LocalStack.
- [Docker](https://docs.docker.com/get-docker/)
- [VS Code](https://code.visualstudio.com/) with the [LocalStack Toolkit](https://marketplace.visualstudio.com/items?itemName=localstack.localstack) ≥ 1.2 and [AWS Toolkit](https://marketplace.visualstudio.com/items?itemName=AmazonWebServices.aws-toolkit-vscode) ≥ 3.74
- [Java](https://openjdk.org/) and [Maven](https://maven.apache.org/)
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

```bash
make start
```

This starts LocalStack with Lambda Debug Mode enabled, using the `localstack/localstack-pro` image with `LOCALSTACK_LAMBDA_DEBUG_MODE=1`.

## Deploy the Application

```bash
make build
make deploy
```

## Debug the Lambda Function

### Via AWS Toolkit for VS Code (recommended)

1. Run the VS Code command **"LocalStack: Run Setup Wizard"** using the LocalStack Toolkit.
2. Start LocalStack from the LocalStack Toolkit status bar.
3. Open the **Remote invoke configuration** in the AWS Toolkit.
4. Select the **Remote debugging** checkbox.
5. Specify the local root path to your handler file.
6. Set a breakpoint in `HelloWorldFunction/src/main/java/helloworld/App.java`.
7. Click **Remote invoke** to start a debugging session.

### Via Lambda Debug Mode

1. Open the sample folder in VS Code to auto-detect `.vscode/launch.json`.
2. Set a breakpoint in `HelloWorldFunction/src/main/java/helloworld/App.java`.
3. Open the **Run and Debug** view and run the **Java: Remote Attach** task.
4. Run `make invoke` to invoke the Lambda function.

## License

This code is available under the Apache 2.0 license.
