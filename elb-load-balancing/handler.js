module.exports.hello1 = async (event) => {
  console.log(event);
  return {
    "isBase64Encoded": false,
    "statusCode": 200,
    "statusDescription": "200 OK",
    "headers": {
        "Content-Type": "application/json"
    },
    "body": "Hello 1"
  };
};

// https://docs.aws.amazon.com/elasticloadbalancing/latest/application/lambda-functions.html#respond-to-load-balancer
// for response format from lambda handler
module.exports.hello2 = async (event) => {
  console.log(event);
    return {
    "isBase64Encoded": false,
    "statusCode": 200,
    "statusDescription": "200 OK",
    "headers": {
        "Content-Type": "application/json"
    },
    "body": "Hello 2"
  };
};
