# SageMaker Model Inference

This is a small example about how you can use LocalStack to host your PyTorch ML models.

Before using this example you should setup your Docker Client to pull the AWS Deep Learning images ([more info here](https://github.com/aws/deep-learning-containers/blob/master/available_images.md)):

```bash
    aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 763104351884.dkr.ecr.us-east-1.amazonaws.com
```

Because the images tend to be really big (multiple GB), you might want to `docker pull` them beforehand to avoid any timeouts.