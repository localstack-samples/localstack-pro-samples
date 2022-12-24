# simple Lambda function training a scikit-learn model on the digits classification dataset
# see https://scikit-learn.org/stable/auto_examples/classification/plot_digits_classification.html
import boto3
import numpy
from joblib import load


def handler(event, context):
    # download the model and the test set from S3
    s3_client = boto3.client("s3")
    s3_client.download_file(Bucket="pods-test", Key="test-set.npy", Filename="test-set.npy")
    s3_client.download_file(Bucket="pods-test", Key="model.joblib", Filename="model.joblib")

    with open("test-set.npy", "rb") as f:
        X_test = numpy.load(f)

    clf = load("model.joblib")

    predicted = clf.predict(X_test)
    print("--> prediction result:", predicted)
