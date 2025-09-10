import json

print("Initializing")

def lambda_handler(event, context):
    message = "Hello LocalStack!"
    print(message)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": message,
            "location": "TestLocation",
        }),
    }
