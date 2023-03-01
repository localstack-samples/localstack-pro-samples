# LocalStack Pro Samples

This repository contains sample projects that can be deployed on your local machine using [LocalStack Pro](https://localstack.cloud/).

Each example in the repository is prefixed with the name of the AWS service being used. For example, the `elb-load-balancing` directory contains examples that demonstrate how to use the Elastic Load Balancing service with LocalStack. Please refer to the sub directories for more details and instructions on how to start the samples.

## Prerequisites

* [Docker](https://docs.docker.com/get-docker/)
* [`awslocal` CLI](https://docs.localstack.cloud/user-guide/integrations/aws-cli/)
* [Serverless](https://www.serverless.com/framework/docs/getting-started)
* [Terraform](https://developer.hashicorp.com/terraform/downloads)
* `make` & `jq`

## Configuration

Some of the samples require LocalStack Pro features. Please make sure to properly configure the `LOCALSTACK_API_KEY` environment variable. You can find your API key in the [LocalStack Pro dashboard](https://app.localstack.cloud/account/apikeys) and you can refer to our [API key documentation](https://docs.localstack.cloud/getting-started/api-key/) for more details.

## Outline

| Sample Name                                                    | Description                                                                                        |
| -------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| [Serverless Websockets](serverless-websockets)                 | API Gateway V2 websocket APIs deployed via the Serverless framework                                |
| [RDS Database Queries](rds-db-queries)                         | Running queries locally against an RDS database                                                    |
| [Neptune Graph Database](neptune-graph-db)                     | Running queries locally against a Neptune Graph database                                           |
| [Lambda Event Filtering](lambda-event-filtering)               | Lambda event source filtering with DynamoDB and SQS                                                |
| [Glacier & S3 select queries](glacier-s3-select)               | Using Glacier API and running S3 Select queries locally                                            |
| [Cloudwatch Metrics alarm](cloudwatch-metrics-aws)             | Triggering a Cloudwatch metrics alarm based on a failing Lambda                                    |
| [EC2 with Docker backend](ec2-docker-instances)                | Running EC2 instances with Docker backend                                                          |
| [QLDB ledger queries](qldb-ledger-queries)                     | Running queries locally against a QLDB ledger                                                      |
| [Cognito with JWT](cognito-jwt)                                | Running Cognito authentication and user pools locally                                              |
| [Transfer API with S3](transfer-ftp-s3)                        | Using the Transfer API to upload files to S3                                                       |
| [Codecommit with Git repository](codecommit-git-repo)          | Using the Codecommit API to create and push to a Git repository                                    |
| [Lambda Mounting and Debugging](lambda-mounting-and-debugging) | Debugging Lambda functions locally                                                                 |
| [IAM Policy Enforcement](iam-policy-enforcement)               | Enforcement of IAM policies when working with local cloud APIs                                     |
| [Lambda Hot Reloading](lambda-hot-reloading)                   | Hot reloading Lambda functions locally                                                             |
| [IoT Basics](iot-basics)                                       | Usage of IoT APIs locally                                                                          |
| [REST API using Chalice](chalice-rest-api)                     | Deploying a REST API using the Chalice framework                                                   |
| [ECS ECR Container application](ecs-ecr-container-app)         | Pushing Docker images to ECR and running them locally on ECS                                       |
| [Athena queries over S3](athena-s3-queries)                    | Running Athena queries over S3 files locally                                                       |
| [Terraform resources](terraform-resources)                     | Deploying various AWS resources via Terraform                                                      |
| [Lambda Function URLs](lambda-function-urls)                   | Invoking Lambda functions via HTTP(s) URLs                                                         |
| [Sagemaker inference](sagemaker-inference)                     | Creating & invoking a Sagemaker endpoint locally with MNIST dataset                                |
| [MSK with Glue Schema Registry](glue-msk-schema-registry)      | Use of MSK, Glue Schema Registry, Glue ETL, and RDS                                                |
| [AppSync GraphQL](appsync-graphql-api)                         | Deploying a GraphQL API using AppSync                                                              |
| [Lambda XRay tracing](lambda-xray)                             | Using Lambda XRay tracing locally                                                                  |
| [Mediastore Uploads](mediastore-uploads)                       | Using MediaStore API locally                                                                       |
| [Serverless Lambda Layers](serverless-lambda-layers)           | Using Lambda layers locally deployed via the Serverless framework                                  |
| [Java Notification App](java-notification-app)                 | Notification app using AWS Java SDK, SNS, SQS, SES, deployed via CloudFormation                    |
| [Lambda Container images](lambda-container-image)              | Deploying Lambda functions as container images                                                     |
| [Glue crawler with RedShift](glue-redshift-crawler)            | Glue Crawler to populate the Glue metadata store with the table schema of RedShift database tables |
| [API Gateway custom domain](apigw-custom-domain)               | Using API Gateway v2 endpoints using custom domain names, deployed via the Serverless framework    |
| [CDK resources](cdk-resources)                                 | Deploying various AWS resources via CDK                                                            |
| [Glue for ETL jobs](glue-etl-jobs)                             | Using Glue API to run local ETL jobs                                                               |
| [Message Queue broker](mq-broker)                              | Using MQ API to run local message queue brokers                                                    |
| [ELB Load Balancing](elb-load-balancing)                       | Using ELBv2 Application Load Balancers locally, deployed via the Serverless framework              |
| [Reproducible ML](reproducible-ml)                             | Train, save and evaluate a scikit-learn machine learning model using AWS Lambda and S3             |
| [Lambda PHP/Bref CDK App](lambda-php-bref-cdk-app)             | Running PHP/Bref Lambda handler locally, deployed via AWS CDK                                      |

## Checking out a single sample

To check out a single sample, you can use the following commands:

```bash
mkdir localstack-samples && cd localstack-samples
git init
git remote add origin -f git@github.com:localstack/localstack-pro-samples.git
git config core.sparseCheckout true
echo <LOCALSTACK_SAMPLE_DIRECTORY_NAME> >> .git/info/sparse-checkout
git pull origin master
```

The above commands use `sparse-checkout` to only pull the sample you are interested in. You can find the name of the sample directory in the table above.

# Developer Notes

## Makefiles for samples
All samples should have a Makefile to unify the execution of the otherwise heterogeneous samples.
It needs to fulfill two criteria:
- The sample should be executable independently, since it can be checked out on its own (see [Checking out a single sample](#checking-out-a-single-sample)).
- It should contain a `test-ci` target to be executed automatically within the CI pipeline. This step needs to take care of all infrastructure tasks (starting/stopping/logs/etc) in addition to any sample commands executed.

A typical Makefile looks like this:
```bash
export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION=us-east-1
SHELL := /bin/bash

usage:       ## Show this help
        @fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:     ## Install dependencies
        @which localstack || pip install localstack
        @which awslocal || pip install awscli-local
        ## install whatever else you need, like node modules, python packages, etc.
        @test -e node_modules || npm install
        @test -e .venv || (python3 -m venv .venv; source .venv/bin/activate; pip install -r requirements.txt)

run:         ## Run the actual sample steps/commands. This assumes LocalStack is up and running.
        ./run.sh

start:       ## Start LocalStack in detached mode
        localstack start -d

stop:        ## Stop the Running LocalStack container
        @echo
        localstack stop

ready:       ## Make sure the LocalStack container is up
        @echo Waiting on the LocalStack container...
        @localstack wait -t 30 && echo LocalStack is ready to use! || (echo Gave up waiting on LocalStack, exiting. && exit 1)

logs:        ## Save the logs in a separate file, since the LS container will only contain the logs of the last sample run.
        @localstack logs > logs.txt

test-ci:     ## Execute the necessary targets in the correct order for an automatic execution. 
        make start install ready run; return_code=`echo $$?`;\
        make logs; make stop; exit $$return_code;

.PHONY: usage install run start stop ready logs test-ci
```