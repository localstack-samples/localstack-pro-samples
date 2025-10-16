# simple Lambda function training a scikit-learn model on the digits classification dataset
# see https://scikit-learn.org/stable/auto_examples/classification/plot_digits_classification.html
import boto3
import numpy
from joblib import load

def handler(event, context):
    # download the model and the test set from S3
    s3_client = boto3.client("s3")
    s3_client.download_file(Bucket="reproducible-ml", Key="test-set.npy", Filename="/tmp/test-set.npy")
    s3_client.download_file(Bucket="reproducible-ml", Key="model.joblib", Filename="/tmp/model.joblib")

    with open("/tmp/test-set.npy", "rb") as f:
        X_test = numpy.load(f)

    clf = load("/tmp/model.joblib")

    predicted = clf.predict(X_test)
    print("--> prediction result:", predicted)
