const uuidv4 = require('uuid/v4');
const AWS = require('aws-sdk');

const DOCKER_BRIDGE = process.env.LOCALSTACK_HOSTNAME;
const SQS_ENDPOINT = `http://${DOCKER_BRIDGE}:4576`;
const DYNAMODB_ENDPOINT = `http://${DOCKER_BRIDGE}:4569`;

const QUEUE_URL = `http://${DOCKER_BRIDGE}:4576/queue/requestQueue`;
const DYNAMODB_TABLE = 'appRequests';


const connectSQS = () => new AWS.SQS({endpoint: SQS_ENDPOINT});

const connectDynamoDB = () => new AWS.DynamoDB({endpoint: DYNAMODB_ENDPOINT});

const shortUid = () => uuidv4().substring(0, 8);

const handleRequest = async (event) => {
    if (event.path === '/requests' && event.httpMethod === 'POST') {
        return startNewRequest(event);
    } else if (event.path === '/requests' && event.httpMethod === 'GET') {
        return listRequests(event);
    } else {
        return {statusCode: 404, body: {}};
    }
};

const startNewRequest = async () => {
    // put message onto SQS queue
    const sqs = connectSQS();
    const requestID = shortUid();
    const message = {'requestID': requestID};
    let params = {
        MessageBody: JSON.stringify(message),
        QueueUrl: QUEUE_URL
    };
    await sqs.sendMessage(params).promise();

    // set status in DynamoDB to QUEUED
    const dynamodb = connectDynamoDB();
    const status = 'QUEUED';
    params = {
        TableName: DYNAMODB_TABLE,
        Item: {
            id: {
                S: shortUid()
            },
            requestID: {
                S: requestID
            },
            timestamp: {
                N: '' + Date.now()
            },
            status: {
                S: status
            }
        }
    };
    await dynamodb.putItem(params).promise();

    return {
        statusCode: 200,
        body: {
            requestID: requestID,
            status: status
        }
    };
};

const listRequests = async () => {
    const dynamodb = connectDynamoDB();
    const params = {
        TableName: DYNAMODB_TABLE,
    };
    const result = await dynamodb.scan(params).promise();
    const items = result['Items'].map((x) => {
        Object.keys(x).forEach((attr) => {
            if ('N' in x[attr]) x[attr] = parseFloat(x[attr].N);
            else if ('S' in x[attr]) x[attr] = x[attr].S;
            else x[attr] = x[attr][Object.keys(x[attr])[0]];
        });
        return x;
    });
    return {
        statusCode: 200,
        body: {result: items}
    };
};

module.exports = {
    handleRequest
};
