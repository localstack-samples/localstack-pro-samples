import os
import boto3
import pickle
import json

def lambda_handler(event, context):
    print(f"Received event: {json.dumps(event)}")

    # Retrieve JSON from body
    payload = json.loads(event["body"])
    sample = payload.get("sample")

    # Specify the S3 bucket and object key
    bucket_name = os.environ["MODEL_BUCKET_NAME"]
    object_key = os.environ["MODEL_OBJECT_KEY"]

    # Create an S3 client
    s3 = boto3.client("s3")

    # Download the file from S3
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    model_data = response["Body"].read()

    # Load the model from the downloaded data
    model = pickle.loads(model_data)

    # Run inference.
    print(f"Running inference on sample: {sample}")
    index_prediction = int(model.predict(sample)[0])
    print(f"Prediction index: {index_prediction}")
    prediction = model.classes_names[index_prediction]
    print(f"Prediction: {prediction}")

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({"prediction": prediction})
    }
