# LocalStack Demo: SageMaker Machine Learning Job (MNIST TensorFlow)

Simple demo application illustrating running a machine learning job using the AWS SageMaker API locally. The ML job computes an image classification model for the popular MNIST dataset that ships with TensorFlow.

## Prerequisites

* LocalStack
* Docker
* Python
* `virtualenv`
* `make`
* [`awslocal`](https://github.com/localstack/awscli-local)

## Installing

To install the dependencies:
```
make install
```

## Starting LocalStack

Make sure that LocalStack is started with the following `SERVICES` configuration:
```
LOCALSTACK_API_KEY=... DEBUG=1 SERVICES=sagemaker,s3,logs,sts,iam localstack start
```

## Running

Run the SageMaker TensorFlow training job as follows:
```
make run
```

This command pulls a SageMaker TensorFlow Docker image, and spins up a Docker container that runs the training job. (This may take some time.)

When the job has finished running, you should see the results in the target S3 bucket:
```
$ awslocal s3 ls s3://sagemaker-us-east-1-000000000000/
                           PRE data/
                           PRE eval/
                           PRE export/
                           PRE sagemaker-tensorflow-2020-01-05-15-25-45-512/
2020-01-05 16:26:06        126 checkpoint
2020-01-05 16:26:10     429419 events.out.tfevents.1578237951.1f80154c1f1a
2020-01-05 16:26:10     334668 graph.pbtxt
2020-01-05 16:26:10   39295624 model.ckpt-0.data-00000-of-00001
2020-01-05 16:26:10        976 model.ckpt-0.index
2020-01-05 16:26:10     133393 model.ckpt-0.meta
2020-01-05 16:26:06   39295624 model.ckpt-10.data-00000-of-00001
2020-01-05 16:26:10        976 model.ckpt-10.index
2020-01-05 16:26:06     133393 model.ckpt-10.meta
```

## License

This code is available under the Apache 2.0 license.
