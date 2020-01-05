import os
import sagemaker
import tensorflow as tf
from sagemaker.tensorflow import TensorFlow
from tensorflow.examples.tutorials.mnist import input_data
from localstack.utils.aws import aws_stack
from localstack.utils.common import short_uid, new_tmp_file, download

SM_REPO = 'https://github.com/awslabs/amazon-sagemaker-examples'
TF_MNIST_URL = '%s/raw/master/sagemaker-python-sdk/tensorflow_distributed_mnist/mnist.py' % SM_REPO


def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))


def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def convert_to(data_set, name, directory):
    """Converts a dataset to tfrecords."""
    images = data_set.images
    labels = data_set.labels
    num_examples = data_set.num_examples

    if images.shape[0] != num_examples:
        raise ValueError('Images size %d does not match label size %d.' %
                         (images.shape[0], num_examples))
    rows = images.shape[1]
    cols = images.shape[2]
    depth = images.shape[3]

    filename = os.path.join(directory, name + '.tfrecords')
    writer = tf.python_io.TFRecordWriter(filename)
    for index in range(num_examples):
        image_raw = images[index].tostring()
        example = tf.train.Example(features=tf.train.Features(feature={
            'height': _int64_feature(rows),
            'width': _int64_feature(cols),
            'depth': _int64_feature(depth),
            'label': _int64_feature(int(labels[index])),
            'image_raw': _bytes_feature(image_raw)}))
        writer.write(example.SerializeToString())
    writer.close()


def test_train_tensorflow():

    sagemaker_client = aws_stack.connect_to_service('sagemaker')
    iam_client = aws_stack.connect_to_service('iam')
    sagemaker_session = sagemaker.Session(boto_session=aws_stack.Boto3Session(),
        sagemaker_client=sagemaker_client)

    try:
        response = iam_client.create_role(RoleName='r1', AssumeRolePolicyDocument='{}')
    except Exception:
        response = iam_client.get_role(RoleName='r1')
    role_arn = response['Role']['Arn']
    test_data = 'testdata'

    if not os.path.exists(test_data):
        data_sets = input_data.read_data_sets(test_data,
            dtype=tf.uint8, reshape=False, validation_size=5000)
        convert_to(data_sets.train, 'train', test_data)
        convert_to(data_sets.validation, 'validation', test_data)
        convert_to(data_sets.test, 'test', test_data)

    inputs = sagemaker_session.upload_data(path=test_data, key_prefix='data/mnist')

    tmp_file = new_tmp_file()
    download(TF_MNIST_URL, tmp_file)
    mnist_estimator = TensorFlow(entry_point=tmp_file, role=role_arn, framework_version='1.12.0',
        training_steps=10, evaluation_steps=10, sagemaker_session=sagemaker_session,
        train_instance_count=1, train_instance_type='local')
    mnist_estimator.fit(inputs, logs=False)


def main():
    test_train_tensorflow()


if __name__ == '__main__':
    main()
