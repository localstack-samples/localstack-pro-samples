# LocalStack Demo: Lambda X-Ray with Python X-Ray SDK

Simple demo application illustrating Lambda XRay tracing using LocalStack, deployed via CloudFormation.

This X-Ray sample demonstrates how to instrument a Python Lambda function with the [AWS X-Ray SDK](https://docs.aws.amazon.com/xray/latest/devguide/xray-sdk-python.html)
and shows how to use the X-Ray API to fetch distributed trace data.

## Prerequisites

- LocalStack
- Docker
- Python / `pip`
- `make`
- [awslocal](https://github.com/localstack/awscli-local)

## Start LocalStack

Start your LocalStack with your API key configured along with the `DEBUG=1` configuration:

```bash
LOCALSTACK_API_KEY=$LOCALSTACK_API_KEY DEBUG=1 localstack start
```

## Create a new bucket

To create a new bucket for deployment artifacts, run the script `1-create-bucket.sh`.

```bash
./1-create-bucket.sh
```

## Create a Lambda Layer

To build a Lambda layer that contains the function's runtime dependencies, run `2-build-layer.sh`. Packaging dependencies in a layer reduces the size of the deployment package that you upload when you modify your code.

```bash
./2-build-layer.sh
```

## Deploy the Lambda function

To deploy the application, run `3-deploy.sh`. This script uses AWS CloudFormation to deploy the Lambda functions and an IAM role. If the AWS CloudFormation stack that contains the resources already exists, the script updates it with any changes to the template or function code.

```bash
./3-deploy.sh
```

The deployment succeeds with the message `Successfully created/updated stack - blank-python`.

## Test the Lambda function

To invoke the function, run `4-invoke.sh`. The application uses AWS X-Ray to trace requests. Pass the desired number of invocations as an argument to the invoke script (default 1).

```bash
./4-invoke.sh 3
```

Each invocation will output the response of the [invoke](https://docs.aws.amazon.com/cli/latest/reference/lambda/invoke.html) CLI command and print the function response:

```json
{
    "StatusCode": 200,
    "ExecutedVersion": "$LATEST"
}
{"TotalCodeSize": 13300014, "FunctionCount": 1}
```

## Retrieve X-Ray traces

The application uses AWS X-Ray to trace requests. To retrieve the traces from the last 10 minutes, run `5-get-traces.sh`.

```bash
./5-get-traces.sh
```

The trace summaries from [get-trace-summaries](https://docs.aws.amazon.com/cli/latest/reference/xray/get-trace-summaries.html) look like this:

```json
{
    "TraceSummaries": [
        {
            "Id": "1-6501e4cc-80de05b73e3d5408133a1f6e",
            "Duration": 0,
            "ResponseTime": 1,
            "HasFault": false,
            "HasError": false,
            "HasThrottle": false,
            "Http": {},
            "Annotations": {},
            "Users": [],
            "ServiceIds": []
        }
    ],
    "TracesProcessedCount": 1,
    "ApproximateTime": 1694622926.0
}
```

The full trace from [batch-get-traces](https://docs.aws.amazon.com/cli/latest/reference/xray/batch-get-traces.html) looks like this:

```json
[
    {
        "Id": "1-6501e4cc-80de05b73e3d5408133a1f6e",
        "Duration": 0,
        "Segments": [
            {
                "Id": "9900c9ba27f4e865",
                "Document": "{\"id\": \"9900c9ba27f4e865\", \"name\": \"lambda\", \"start_time\": 1694622924.3674095, \"parent_id\": \"32a0edc7c2e9eb40\", \"in_progress\": false, \"http\": {\"response\": {\"status\": 200}}, \"aws\": {\"operation\": \"GetAccountSettings\", \"region\": \"us-east-1\", \"request_id\": \"57048e74-aa89-474b-a2d2-2789268795b7\"}, \"trace_id\": \"1-6501e4cc-80de05b73e3d5408133a1f6e\", \"type\": \"subsegment\", \"namespace\": \"aws\", \"end_time\": 1694622924.3729706}"
            },
            {
                "Id": "7bbe501dcb99435d",
                "Document": "{\"id\": \"7bbe501dcb99435d\", \"name\": \"annotations\", \"start_time\": 1694622924.3760014, \"parent_id\": \"32a0edc7c2e9eb40\", \"in_progress\": false, \"annotations\": {\"custom_annotation\": 12345}, \"trace_id\": \"1-6501e4cc-80de05b73e3d5408133a1f6e\", \"type\": \"subsegment\", \"namespace\": \"local\", \"end_time\": 1694622924.3760374}"
            }
        ]
    }
]
```

## Credits

This sample is based on the [blank-python](https://github.com/awsdocs/aws-lambda-developer-guide/tree/main/sample-apps/blank-python) example from the [aws-lambda-developer-guide](https://github.com/awsdocs/aws-lambda-developer-guide/tree/main).

## License

The documentation is made available under the [Creative Commons Attribution-ShareAlike 4.0 International Public License](https://github.com/awsdocs/aws-lambda-developer-guide/blob/main/LICENSE).

- This README.md documentation was adjusted for use with LocalStack, mainly by describing how to set up LocalStack.

The sample code is made available under a [modified MIT license](https://github.com/awsdocs/aws-lambda-developer-guide/blob/main/LICENSE-SAMPLECODE).

- The code was adjusted by replacing `aws` with `awslocal` for use with LocalStack, adding a `Makefile` to automate all steps, updating the Python dependencies, parametrizing the invoke script, adding a get-traces script, demonstrating custom subsegement tracing, and removed the unused tests.
