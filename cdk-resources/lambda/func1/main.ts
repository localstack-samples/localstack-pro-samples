import {SQSEvent} from 'aws-lambda'

export const handler = async (event: SQSEvent) => {
    console.log(`Event: ${JSON.stringify(event, null, 2)}`);
    return {
        statusCode: 200,
        body: JSON.stringify({
            message: 'hello world',
        }),
    }
};
