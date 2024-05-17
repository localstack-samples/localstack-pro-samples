const { echo } = require('/opt/nodejs/lib');

module.exports.hello = async function(event, context) {
  echo('This text should be printed in the Lambda');
}

module.exports.authorizerFunc = async function(event, context, callback) {
    console.log('Running authorizer function', event);
    var token = event.authorizationToken;
    callback(null, generatePolicy('user', 'Allow', event.methodArn));
};

// Helper function to generate an IAM policy
// See https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-use-lambda-authorizer.html
var generatePolicy = function(principalId, effect, resource) {
    var authResponse = {};

    authResponse.principalId = principalId;
    if (effect && resource) {
        var policyDocument = {};
        policyDocument.Version = '2012-10-17';
        policyDocument.Statement = [];
        var statementOne = {};
        statementOne.Action = 'execute-api:Invoke';
        statementOne.Effect = effect;
        statementOne.Resource = resource;
        policyDocument.Statement[0] = statementOne;
        authResponse.policyDocument = policyDocument;
    }

    // Optional output with custom properties of the String, Number or Boolean type.
    authResponse.context = {
        "stringKey": "stringval",
        "numberKey": 123,
        "booleanKey": true
    };
    return authResponse;
}
