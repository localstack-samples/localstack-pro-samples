const AWS = require('aws-sdk');

const cloudFrontUrl = 'https://4210a2de.cloudfront.localhost.localstack.cloud';
const htmlBucket = 'htmlpages';
const dataBucket = 'userdata';

const s3Endpoint = `${process.env.LOCALSTACK_HOSTNAME}:4566`;
const s3Params = {
  endpoint: s3Endpoint, sslEnabled: false, s3ForcePathStyle: true
};
const s3 = new AWS.S3(s3Params);

module.exports.getHtml = async event => {
  const pathParam = event.pathParameters;
  const path = pathParam && (pathParam.path || pathParam['path+']);
  const key = `${path}.html`;
  const params = {
    Bucket: htmlBucket,
    Key: key
  };
  const response = await s3.getObject(params).promise();
  return {
    statusCode: 200,
    body: response.Body.toString('utf-8'),
    headers: {'Content-Type': 'text/html'}
  };
};

module.exports.getData = async event => {
    const key = event.pathParameters.user_id;
    const params = {
      Bucket: dataBucket,
      Key: key
    };
    const response = await s3.getObject(params).promise();
    return {
      statusCode: 200,
      body: JSON.stringify({ message: response.Body.toString('utf-8') })
    };
};

module.exports.putData = async event => {
  const key = event.pathParameters.user_id;
  const params = {
    ACL: 'public-read',
    Body: Math.random().toString().replace('0.',''),
    Bucket: dataBucket,
    Key: key,
    ContentType: 'text/plain'
  };
  await s3.upload(params).promise();
  const signer = new AWS.CloudFront.Signer(process.env.cloudFrontAccessKeyId, process.env.cloudFrontPrivateKey);
  const resultUrl = signer.getSignedUrl({url: `${cloudFrontUrl}/${key}/data`, expires: Date.now() + 360000})
  return {
    statusCode: 201,
    body: JSON.stringify(
      {
        result: resultUrl
      }
    ),
  };
};
