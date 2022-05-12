AWS Messaging: Spring Boot on LocalStack 
========================================

This sample Spring Boot application project demonstrates how to: 

* Provision CloudFormation infrastructure on LocalStack
* Configure SNS SQS subscriptions with CloudFormation
* Receive SQS messages with the AWS Java SDK
* Send SES message with the AWS Java SDK

## Requirements

* Java 11+
* Maven 3+
* [LocalStack](https://github.com/localstack/localstack)
* [awslocal](https://github.com/localstack/awscli-local)

## How To

### Build the application

The application is a simple Spring Boot application that you can build by running

    mvn clean install

### Spin up the infrastructure on localstack

Resources are deployed via a CloudFormation template in `src/main/resources/email-infra.yml`.

First, start LocalStack and the SMTP server with:

    LOCALSTACK_API_KEY=<your-api-key> docker-compose up -d

Then deploy the cloudformation stack (can take a few seconds)

    awslocal cloudformation deploy \
        --template-file src/main/resources/email-infra.yml \
        --stack-name email-infra

### Start the Spring Boot application

You can use `mvn spring-boot:run` to start the application, but you will need to set dummy AWS access credentials as environment variables:

    AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test mvn spring-boot:run

### Test the application

Verify the sender email address configured in the app

    awslocal ses verify-email-identity --email-address no-reply@localstack.cloud

Send a message to the topic

    awslocal sns publish \
        --topic arn:aws:sns:us-east-1:000000000000:email-notifications \
        --message '{"subject":"hello", "address": "alice@example.com", "body": "hello world"}'

Check the `/list` endpoint for queued messages.

    curl -s localhost:8080/list | jq .


Run the `/process` endpoint to send the queued notifications as emails

    curl -s localhost:8080/process

Verify that the email has been sent:

* either check MailHog via the UI http://localhost:8025/
* or query the LocalStack internal SES endpoint: `curl -s localhost:4566/_localstack/ses | jq .`
