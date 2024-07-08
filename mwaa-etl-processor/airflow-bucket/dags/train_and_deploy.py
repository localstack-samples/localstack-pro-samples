from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.models import Variable
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.amazon.aws.hooks.lambda_function import LambdaHook
from airflow.providers.amazon.aws.hooks.base_aws import AwsBaseHook

import pickle
import io

from pydantic import BaseModel
from typing import List, Dict, Optional

import hashlib
import pandas as pd

class DatasetSpec(BaseModel):
    url: str
    name: str
    feature_columns: List[str]
    target_column: str

@dag(schedule_interval=None, start_date=days_ago(1), tags=['example'])
def train_and_deploy_classifier_model():
    @task
    def retrieve_dataset():
        # Retrieve the dataset from the Airflow Variable.
        dataset_spec = Variable.get(
            "dataset_spec",
            deserialize_json=True,
        )
        if dataset_spec is None:
            raise ValueError("Dataset URL is not defined")
        
        try:
            DatasetSpec(**dataset_spec)
        except Exception as e:
            raise ValueError(f"Invalid dataset spec: {e}")
        
        return dataset_spec

    @task
    def read_dataset(dataset_spec):
        dataset = DatasetSpec(**dataset_spec)

        # Read the dataset from the specified URL.
        df = pd.read_csv(dataset.url)
        print(df.head())

        # Compute dataset ID.
        dataset_id = hashlib.sha256(pd.util.hash_pandas_object(df, index=True).values).hexdigest()
        print(f"Dataset ID: {dataset_id}")

        # Return the dataset and its ID.
        return {
            "dataset": df.to_dict(), 
            "dataset_id": dataset_id,
        }
    
    @task
    def train_model(dataset_spec: dict, dataset: dict, algorithm: str):
        from sklearn import svm
        from sklearn import metrics
        from sklearn.preprocessing import LabelEncoder
        from sklearn.linear_model import LogisticRegression
        from sklearn.model_selection import train_test_split
        from sklearn.neighbors import KNeighborsClassifier
        from sklearn.tree import DecisionTreeClassifier

        df_json: Dict = dataset["dataset"]
        dataset_id: str = dataset["dataset_id"]
        dataset_spec: DatasetSpec = DatasetSpec(**dataset_spec)
        data: pd.DataFrame = pd.DataFrame().from_dict(df_json)

        print(data.head())

        # Split the dataset into feature columns and target column.
        X_data = data[dataset_spec.feature_columns]
        Y_data = data[dataset_spec.target_column]

        # Split the dataset into training and testing sets.
        X_train, X_test, y_train, y_test = train_test_split(X_data, Y_data, test_size=0.2)

        # Encode the target column.
        label_encoder = LabelEncoder()
        y_train_encoded = label_encoder.fit_transform(y_train)
        y_test_encoded = label_encoder.transform(y_test)
        y_train = y_train_encoded
        y_test = y_test_encoded

        # Print the dataset information.
        print(f"Feature columns: {dataset_spec.feature_columns}")
        print(f"Target column: {dataset_spec.target_column}")
        print(f"Train size: {len(X_train)}")
        print(f"Test size: {len(X_test)}")
        print(f"Training model using {algorithm} algorithm")

        # Train the model using the specified algorithm.
        if algorithm == "SVM":
            model = svm.SVC()
        elif algorithm == "LogisticRegression":
            model = LogisticRegression()
        elif algorithm == "DecisionTreeClassifier":
            model = DecisionTreeClassifier()
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")
        
        # Train the model.
        model.fit(X_train, y_train)

        # Predict the target values.
        y_pred = model.predict(X_test)

        # Compute the accuracy of the model.
        accuracy = metrics.accuracy_score(y_test, y_pred)
        precision = metrics.precision_score(y_test, y_pred, average="weighted")
        recall = metrics.recall_score(y_test, y_pred, average="weighted")
        f1 = metrics.f1_score(y_test, y_pred, average="weighted")
        conf_matrix = metrics.confusion_matrix(y_test, y_pred)

        # Save the model and label encoder classes.
        model.classes_names = label_encoder.classes_
        
        # Dump the model and label encoder to S3.
        s3_hook = S3Hook(aws_conn_id="aws_default")
        s3_hook.create_bucket(bucket_name="models")
        model_bytes = pickle.dumps(model)
        model_buffer = io.BytesIO(model_bytes)
        s3_hook.load_bytes(
            bytes_data=model_buffer.getvalue(),
            key=f"models/{dataset_id}/{algorithm}.pkl",
            bucket_name="models",
            replace=True,
        )

        # Print or log the evaluation metrics
        print(f"Accuracy: {accuracy}")
        print(f"Precision: {precision}")
        print(f"Recall: {recall}")
        print(f"F1 Score: {f1}")
        print(f"Confusion Matrix:\n{conf_matrix}")

        return accuracy
    
    @task
    def deploy_model(ml_algorithms: List[str], accuracies: List[float], dataset: dict):
        print(f"Model accuracies: {accuracies}")
        print(f"ML algorithms: {ml_algorithms}")

        dataset_id = dataset["dataset_id"]
        best_model_index = accuracies.index(max(accuracies))
        best_ml_algorithm = ml_algorithms[best_model_index]

        print(f"Location of best model: s3://models/models/{dataset_id}/{best_ml_algorithm}.pkl")
        lambda_hook = LambdaHook(aws_conn_id="aws_default")
        lambda_client = lambda_hook.get_client_type()

        try:
            lambda_hook.create_lambda(
                function_name=f"ml-model-{best_ml_algorithm}-{dataset_id}"[:64],
                runtime="python3.9",
                role="arn:aws:iam::000000000000:role/lambda-role",
                handler="main.lambda_handler",
                code={
                    "S3Bucket": "lambda",
                    "S3Key": "deploy_lambda.zip",
                },
                environment={
                    "Variables": {
                        "MODEL_BUCKET_NAME": "models",
                        "MODEL_OBJECT_KEY": f"models/{dataset_id}/{best_ml_algorithm}.pkl",
                    },
                },
            )
        except Exception as e:
            print(f"Error creating the function: {e}")

        try:
            lambda_client.create_function_url_config(
                FunctionName=f"ml-model-{best_ml_algorithm}-{dataset_id}"[:64],
                AuthType="NONE",
                InvokeMode="BUFFERED",
            )
        except Exception as e:
            print(f"Error creating the function URL config: {e}")
    
    dataset_spec: Dict = retrieve_dataset()
    dataset = read_dataset(dataset_spec)

    ml_algorithms = ["SVM", "LogisticRegression", "DecisionTreeClassifier"]
    accuracies = []
    for algorithm in ml_algorithms:
        accuracies += [train_model(dataset_spec, dataset, algorithm)]

    deploy_model(ml_algorithms, accuracies, dataset)


dag = train_and_deploy_classifier_model()
