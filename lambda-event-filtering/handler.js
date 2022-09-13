'use strict';

const AWS = require('aws-sdk');
const ULID = require('ulid');
const dynamo = new AWS.DynamoDB.DocumentClient();

const TABLE_NAME = process.env.TABLE_NAME

exports.save = async (event) => {
    console.log(event);

    const object = event.body;

    const item = {
        id: ULID.ulid(),
        object,
        date: Date.now()
    }

    console.log(item);

    const savedItem = await saveItem(item);

    return {
        statusCode: 200,
        body: JSON.stringify(savedItem),
      }
}

exports.processDynamo = async (event) => {
    console.log(event);
}

exports.processASQS = async(event) => {
    console.log('Process A');
    console.log(event);
}

async function saveItem(item) {
    const params = {
		TableName: TABLE_NAME,
		Item: item
	};

    console.log(params)
    
    return dynamo.put(params).promise().then(() => {
        return item;
    });
};
