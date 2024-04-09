import AWSLambda from "aws-lambda";

import { downcaseKeys } from "./util";

const errorResponse = (message: string, code = 500): AWSLambda.APIGatewayProxyResult => ({
  body: JSON.stringify({ error: message }),
  statusCode: code,
});

export default async (event: AWSLambda.APIGatewayEvent): Promise<AWSLambda.APIGatewayProxyResult> => {
  const headers = downcaseKeys(event.headers);

  if (!/^application\/json\b/.test(headers["content-type"] || "") || !event.body) {
    return errorResponse("Only JSON payloads are accepted", 406);
  }

  const payload = JSON.parse(event.body);
  return Object.keys(payload).length === 0
    ? errorResponse("No data provided", 422)
    : {
        body: JSON.stringify({ payload }),
        statusCode: 200,
      };
};
