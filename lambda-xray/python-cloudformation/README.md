# LocalStack Demo: Lambda XRay Tracing with CloudFormation

Simple demo application illustrating Lambda XRay tracing using LocalStack, deployed via CloudFormation.

## Prerequisites

- LocalStack
- Docker
- Python / `pip`
- `make`

## Start LocalStack

Start your LocalStack with your API key configured along with the `DEBUG=1` configuration:

```bash 
LOCALSTACK_API_KEY=... DEBUG=1 localstack start
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

## Test the Lambda function

To invoke the function, run `4-invoke.sh`. The application uses AWS X-Ray to trace requests. Let the script invoke the function a few times and then press `CRTL+C` to exit.

```bash 
./4-invoke.sh
```

The application uses AWS X-Ray to trace requests. To retrieve the traces, run `5-get-traces.sh`. 

```bash 
./5-get-traces.sh
```
