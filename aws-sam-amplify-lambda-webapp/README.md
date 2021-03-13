# LocalStack Demo: AWS SAM Reference Web Application

Simple demo application illustrating how to deploy and run the [AWS Serverless Application Model (SAM) reference architecture Web application](https://github.com/aws-samples/lambda-refarch-webapp) locally using LocalStack.

## Prerequisites

* LocalStack
* Docker
* [`awslocal`](https://github.com/localstack/awscli-local)
* [`samlocal`](https://github.com/localstack/aws-sam-cli-local)

## Installing

To install the `samlocal` command line utility:
```
pip install aws-sam-cli-local
```

## Starting LocalStack

Make sure that LocalStack is started with the following `SERVICES` configuration:
```
LOCALSTACK_API_KEY=... DEBUG=1 SERVICES=serverless,cognito,amplify localstack start
```

## Running

Clone the official repository of the SAM reference Web application:
```
git clone https://github.com/aws-samples/lambda-refarch-webapp
cd lambda-refarch-webapp
```

Package and deploy the application against LocalStack, using the `samlocal` command line:
```
awslocal s3 mb s3://test
samlocal build
samlocal package --s3-bucket test --output-template-file packaged.yml
samlocal deploy --stack-name s3 --s3-bucket test --template-file packaged.yml --capabilities CAPABILITY_IAM --parameter-overrides 'Repository=test OauthToken=test'
```

The command above will package the Lambda functions, upload the ZIP files to local S3, create a Cognito user pool, deploy the API Gateway resources, etc. - the process may take some time (1-2 minutes) to complete.

Once deployed, you need to adjust the contents of the `www/src/config.js` configuration file. Use the template below, and make sure to insert the proper values for `<cognitoClientId>` (the Cognito user pool client ID) and `<restApiId>` (the API Gateway REST API ID):
```
const config = {
  "aws_user_pools_web_client_id": "<cognitoClientId>",
  "api_base_url": "http://localhost:4566/restapis/<restApiId>/Stage/_user_request_",
  "coginto_hosted_domain": "localhost.localstack.cloud:4566",
  "redirect_url": "http://localhost:8080/"
};
```

Finally, you can fire up the Web application via:
```
cd www/src
npm install
SKIP_PREFLIGHT_CHECK=true npm start
```

At this point, you should be able to open the Web application under `http://localhost:8080`, create a new user and log in via the LocalStack Cognito login form linked from app, and finally manage the "TODO items" directly in the app (which will get stored in a local DynamoDB table).

## License

This code is available under the Apache 2.0 license.
