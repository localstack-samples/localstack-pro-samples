const fs = require('fs');
const AWSXRay = require('aws-xray-sdk-core');
const _AWS = require('aws-sdk')
var https = require('https');
_AWS.config.update({ httpOptions: { agent: new https.Agent({ rejectUnauthorized: false }) } });
const AWS = AWSXRay.captureAWS(_AWS);
const ddb = new AWS.DynamoDB(/*{
  // Note: this line is NOT required in transparent execution mode (DNS support in LocalStack Pro)
  endpoint: `http://${process.env.LOCALSTACK_HOSTNAME}:4569`
}*/);

module.exports.hello = async function(event, context) {
  const result = await ddb.listTables().promise();
  console.log(`Result of ListTables DynamoDB API call: ${JSON.stringify(result)}`);
  return {
    body: JSON.stringify(result)
  };
};
