# LocalStack Demo: Lambda XRay Tracing

Simple demo application illustrating Lambda XRay tracing using LocalStack, deployed via the Serverless framework.

## Prerequisites

* LocalStack
* Docker
* Node.js / `npm`
* `make`

## Installing

To install the dependencies:
```
make install
```

## Running

Make sure that LocalStack is started with the following `SERVICES` configuration:
```
LOCALSTACK_API_KEY=... DEBUG=1 SERVICES=edge,serverless,xray localstack start
```

Deploy the app locally and run a Lambda test invocation:
```
make run
```

You should see a success output in the terminal:
```
{
    "StatusCode": 200
}
```

... as well as a trace entry that has been pushed to XRay from the Lambda function:
```
{
    "Traces": [
        {
            "Id": "21532313629396",
            "Duration": 0,
            "Segments": [
                {
                    "Id": "1c1561bf84546a5c",
                    "Document": "{\"id\": \"1c1561bf84546a5c\", \"name\": \"dynamodb\", \"start_time\": 1572790352.417, \"namespace\": \"aws\", \"aws\": {\"operation\": \"ListTables\", \"region\": \"us-east-1\", \"request_id\": \"39012a4a-19b6-484a-9252-3102dbe91cbd\", \"retries\": 0, \"table_count\": 0}, \"http\": {\"response\": {\"status\": 200, \"content_length\": \"17\"}}, \"end_time\": 1572790352.486, \"type\": \"subsegment\", \"parent_id\": \"11560be54abce8ed\", \"trace_id\": \"21532313629396\"}"
                }
            ]
        }
    ],
    "UnprocessedTraceIds": []
}
```

## Notes

### Transparent execution mode

Note that the Lambda makes use of transparent execution mode, which means that the SDK client need **not** be configured with the target endpoint address on `localhost`. Simply use the default configuration, and the Lambda code will automatically pick up the right target endpoint by means of our built-in DNS setup.

The only change required to enable transparent execution mode is to allow self-signed certificates in the AWS SDK:
```
const AWS = require('aws-sdk');
var https = require('https');
AWS.config.update({ httpOptions: { agent: new https.Agent({ rejectUnauthorized: false }) } });
```

## License

This code is available under the Apache 2.0 license.
