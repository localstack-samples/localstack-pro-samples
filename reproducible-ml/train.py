# simple Lambda function training a scikit-learn model on the digits classification dataset
# see https://scikit-learn.org/stable/auto_examples/classification/plot_digits_classification.html

import os
import boto3
import numpy
from sklearn import datasets, svm, metrics
from sklearn.utils import Bunch
from sklearn.model_selection import train_test_split
from joblib import dump, load
import io


def handler(event, context):

    digits = load_digits()

    # flatten the images
    n_samples = len(digits.images)
    data = digits.images.reshape((n_samples, -1))

    # Create a classifier: a support vector classifier
    clf = svm.SVC(gamma=0.001)

    # Split data into 50% train and 50% test subsets
    X_train, X_test, y_train, y_test = train_test_split(
        data, digits.target, test_size=0.5, shuffle=False
    )

    # Learn the digits on the train subset
    clf.fit(X_train, y_train)

    # Dump the trained model to S3
    s3_client = boto3.client("s3")
    buffer = io.BytesIO()
    dump(clf, buffer)
    s3_client.put_object(Body=buffer.getvalue(), Bucket="pods-test", Key="model.joblib")
    
    # Save the test-set to the S3 bucket
    numpy.save('test-set.npy', X_test)
    with open('test-set.npy', 'rb') as f:
        s3_client.put_object(Body=f, Bucket="pods-test", Key="test-set.npy")


def load_digits(*, n_class=10, return_X_y=False, as_frame=False):
    # download files from S3
    s3_client = boto3.client("s3")
    s3_client.download_file(Bucket="pods-test", Key="digits.csv.gz", Filename="digits.csv.gz")
    s3_client.download_file(Bucket="pods-test", Key="digits.rst", Filename="digits.rst")

    # code below based on sklearn/datasets/_base.py

    data = numpy.loadtxt('digits.csv.gz', delimiter=',')
    with open('digits.rst') as f:
        descr = f.read()
    target = data[:, -1].astype(numpy.int, copy=False)
    flat_data = data[:, :-1]
    images = flat_data.view()
    images.shape = (-1, 8, 8)

    if n_class < 10:
        idx = target < n_class
        flat_data, target = flat_data[idx], target[idx]
        images = images[idx]

    feature_names = ['pixel_{}_{}'.format(row_idx, col_idx)
                     for row_idx in range(8)
                     for col_idx in range(8)]

    frame = None
    target_columns = ['target', ]
    if as_frame:
        frame, flat_data, target = datasets._convert_data_dataframe(
            "load_digits", flat_data, target, feature_names, target_columns)

    if return_X_y:
        return flat_data, target

    return Bunch(data=flat_data,
                 target=target,
                 frame=frame,
                 feature_names=feature_names,
                 target_names=numpy.arange(10),
                 images=images,
                 DESCR=descr)
