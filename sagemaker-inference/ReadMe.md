# SageMaker Model Inference

This is a small example about how you can use LocalStack to host your PyTorch ML models. It does the following:

* Create MNIST model in SageMaker
* Create a SageMaker Endpoint for accessing the model
* Invoke the endpoint
  * directly on the container
  * via boto

## Requirements

* Python 3.8+
  * boto3
  * numpy
  * mypy
* LocalStack
* Docker

## How To

### Obtain Deep Learning image

Before using this example you should set up your Docker Client to pull the AWS Deep Learning images ([more info here](https://github.com/aws/deep-learning-containers/blob/master/available_images.md)):

```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 763104351884.dkr.ecr.us-east-1.amazonaws.com
```

Because the images tend to be heavy (multiple GB), you might want to `docker pull` them beforehand:

```bash
docker pull 763104351884.dkr.ecr.us-east-1.amazonaws.com/pytorch-inference:1.5.0-cpu-py3
```

### Test the application

Afterwards you can start localstack:

```bash
localstack start    
```

And execute the example with:

```bash
python main.py
```

You should see an output like this:
```
Creating bucket...
Uploading model data to bucket...
Creating model in SageMaker...
Adding endpoint configuration...
Creating endpoint...
Checking endpoint status...
Endpoint not ready - waiting...
Checking endpoint status...
Endpoint ready!
Invoking via boto...
Predicted digits: [7, 3]
Invoking endpoint directly...
Predicted digits: [2, 6]
```