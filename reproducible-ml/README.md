# LocalStack Demo: Train, save and evaluate a scikit-learn machine learning model

In this tutorial, we will train a simple machine-learning model that recognizes handwritten digits on an image. 
We will use the following services:

* an S3 bucket to host our training data;
* a Lambda function to train and save the model to an S3 bucket;
* a Lambda layer that contains the dependencies for our training code;
* a second Lambda function to download the saved model and perform a prediction with it.

## Prerequisites

* LocalStack
* Docker
* `awslocal` CLI

## Installing

To install the dependencies:
```
make install
```

## Starting LocalStack

Make sure that LocalStack is started:
```
LOCALSTACK_API_KEY=... DEBUG=1 localstack start
```

## Running

The entire workflow is executed by the `run.sh` script. To trigger it, execute:
```
make run
```
The model will be first trained by the `ml-train` Lambda function and then uploaded on the S3 bucket.
A second Lambda function will download the model and run predictions on a test set of character inputs.
The logs of the Lambda invocation should be visible in the LocalStack container output (with DEBUG=1 enabled):

```bash
null
>START RequestId: 65dc894d-25e0-168e-dea1-a3e8bfdb563b Version: $LATEST
> --> prediction result: [8 8 4 9 0 8 9 8 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 9 6 7 8 9
...
...
>  9 5 4 8 8 4 9 0 8 9 8]
> END RequestId: 6...
```