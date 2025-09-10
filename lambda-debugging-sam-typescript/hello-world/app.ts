import { APIGatewayProxyEvent, APIGatewayProxyResult } from 'aws-lambda';

export const lambdaHandler = async (event: APIGatewayProxyEvent): Promise<APIGatewayProxyResult> => {
    const message = 'Hello LocalStack!';
    console.log(message);

    return {
        statusCode: 200,
        body: JSON.stringify({ message: message }),
    };
};
