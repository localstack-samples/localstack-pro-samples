# Debug your TypeScript Lambda Function

This Hello World Lambda function written in JavaScript demonstrates how to use interactive breakpoint-debugging using LocalStack [Lambda Remote Debugging](https://docs.localstack.cloud/aws/tooling/lambda-tools/remote-debugging/).
LocalStack automatically configures debugging and adjusts relevant timeouts.

We recommend the one-click setup using the AWS Toolkit for VS Code unless your advanced scenario requires Lambda Debug Mode (Preview).

> [!NOTE]
> Check out our blog post [Developing with LocalStack using the AWS Toolkit for VS Code](#TODO-update-link)

## Prerequisites

* [Docker](https://www.docker.com/)
* [VS Code](https://code.visualstudio.com/)
* [LocalStack Toolkit for VS Code](https://marketplace.visualstudio.com/items?itemName=localstack.localstack) ≥ 1.2 installs [LocalStack](https://docs.localstack.cloud/aws/getting-started/installation/) ≥ 4.8
* [AWS Toolkit for VS Code](https://marketplace.visualstudio.com/items?itemName=AmazonWebServices.aws-toolkit-vscode) ≥ 3.74
* `make`
* [AWS CLI v2](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) or [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)

## Starting Up

1. Execute the VS Code command "LocalStack: Run Setup Wizard" using the LocalStack Toolkit
2. Start LocalStack by clicking on the LocalStack Toolkit status bar

## Deploying

1. Run `make build`
2. Run `make deploy`

## Debugging

1. Open the **Remote invoke configuration** in the AWS Toolkit
    1. Open the AWS Toolkit extension
    2. Expand the AWS Explorer and Lambda node
    3. Navigate to the function you want to debug, then choose the Invoke remotely icon ▶️ from the context menu
2. Select the **Remote debugging** check box to display the remote debugging properties
3. Specify the Local Root Path to your local handler file.
4. Expand the `Remote debug additional configuration`, and set `Out files` to `.aws-sam/build/HelloWorldFunction`
5. Set a breakpoint in your handler file by clicking in the gutter-margin
6. Click the **Remote invoke** button to invoke the Lambda function

> [!NOTE]
> **Debugging TypeScript with source maps**
> Expand the `Remote debug additional configuration`, and set `Out files` to the directory containing the files `<filename>.js` and `<filename>.js.map`.
> Double-check your path if you get the error "outFiles not valid or no js and map file found in outFiles, debug will continue without sourceMap support".
> Notice the path is *relative to the VSCode workspace root*.
> In this example:
> * `.aws-sam/build/HelloWorldFunction` using workspace `code localstack-pro-samples/lambda-debugging-sam-typescript`
> * `lambda-debugging-sam-typescript/.aws-sam/build/HelloWorldFunction` using workspace `code localstack-pro-samples`

## Lambda Debug Mode (Preview, Pro)

### Starting Up

1. Start LocalStack with the following configuration:

    ```sh
    LOCALSTACK_IMAGE_NAME=localstack/localstack-pro \
    LOCALSTACK_LAMBDA_DEBUG_MODE=1 \
    LOCALSTACK_LAMBDA_DEBUG_MODE_CONFIG_PATH=/tmp/lambda_debug_mode_config.yaml \
    localstack start --volume $PWD/lambda_debug_mode_config.yaml:/tmp/lambda_debug_mode_config.yaml
    ```

    * `IMAGE_NAME=localstack/localstack-pro` ensures the Pro image is started
    * `LOCALSTACK_LAMBDA_DEBUG_MODE=1` adjusts timeouts
    * `LOCALSTACK_LAMBDA_DEBUG_MODE_CONFIG_PATH=/tmp/lambda_debug_mode_config.yaml` points to the config file for Lambda debug mode allowing for advanced configuration. It maps the Lambda function `arn:aws:lambda:us-east-1:000000000000:function:HelloWorldFunctionTypeScript` to port `7050`.
    * `--volume $PWD/lambda_debug_mode_config.yaml:/tmp/lambda_debug_mode_config.yaml` maps the Lambda debug configuration from the host into the LocalStack Docker container for hot-reloading configuration updates.

### Deploying

1. Run `make build` to build the Lambda ZIP package
2. Run `make deploy` to deploy the Lambda function

### Debugging

1. Open the sample folder in VS Code to auto-detect `.vscode/launch.json`
    a. If using SAM, ensure `localRoot` is set to `${workspaceFolder}/hello-world`
    b. If using a local build, ensure `localRoot` is set to `${workspaceFolder}/hello-world/dist`
2. Set a breakpoint in the handler file `hello-world/app.ts` by clicking in the gutter-margin
3. Open the **Run and Debug** view in VS Code
4. Run the **Node: Remote Attach** task
5. Run `make invoke` to invoke the Lambda function

## Troubleshooting

* Concurrent invokes are currently rejected with a `ResourceConflictException`.
Upvote [this GitHub issue](https://github.com/localstack/localstack/issues/8522) if this affects you.

## License

The code in this sample is available under the Apache 2.0 license.
