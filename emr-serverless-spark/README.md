# Running EMR Serverless Jobs with Java

We will run a Java Spark job on EMR Serverless using a simple Java "Hello World" example in this example.

## Prerequisites

* LocalStack
* `aws` CLI & `awslocal` script
* Docker
* Java and Maven

## Installation

Before creating the EMR Serverless job, we need to create a JAR file containing the Java code. We have the `java-demo-1.0.jar` file in the current directory. Alternatively, you can create the JAR file yourself by following the steps below.

```bash
cd hello-world
mvn package
```

Next, we need to create an S3 bucket to store the JAR file. To do this, run the following command:

```bash
export S3_BUCKET=test
awslocal s3 mb s3://$S3_BUCKET
```

You can now copy the JAR file from your current directory to the S3 bucket:

```bash
awslocal s3 cp java-demo-1.0.jar s3://${S3_BUCKET}/code/java-spark/ 
```

## Creating the EMR Serverless Job

Specify the ARN for the EMR Serverless job with the following command:

```bash
export JOB_ROLE_ARN=arn:aws:iam::000000000000:role/emr-serverless-job-role
```

We can now create an EMR Serverless application, which will run Spark 3.3.0. Run the following command:

```bash
awslocal emr-serverless create-application \
    --type SPARK \
    --name serverless-java-demo \
    --release-label "emr-6.9.0" \
    --initial-capacity '{
        "DRIVER": {
            "workerCount": 1,
            "workerConfiguration": {
                "cpu": "4vCPU",
                "memory": "16GB"
            }
        },
        "EXECUTOR": {
            "workerCount": 3,
            "workerConfiguration": {
                "cpu": "4vCPU",
                "memory": "16GB"
            }
        }
    }'
```

You can retrieve the Application ID from the output of the command, and export it as an environment variable:

```bash
export APPLICATION_ID='<application-id>'
```

Start the EMR Serverless application:

```shell
awslocal emr-serverless start-application \
    --application-id $APPLICATION_ID
```

## Running the EMR Serverless Job

You can now run the EMR Serverless job:

```bash
awslocal emr-serverless start-job-run \
    --application-id $APPLICATION_ID \
    --execution-role-arn $JOB_ROLE_ARN \
    --job-driver '{
        "sparkSubmit": {
            "entryPoint": "s3://'${S3_BUCKET}'/code/java-spark/java-demo-1.0.jar",
            "sparkSubmitParameters": "--class HelloWorld"
        }
    }' \
    --configuration-overrides '{
        "monitoringConfiguration": {
            "s3MonitoringConfiguration": {
                "logUri": "s3://'${S3_BUCKET}'/logs/"
            }
        }
    }'
```

The Spark logs will be written to the S3 bucket specified in the `logUri` parameter. You can stop the EMR Serverless application with the following command:

```bash
awslocal emr-serverless stop-application \
    --application-id $APPLICATION_ID
```
