# LocalStack Demo: Lambda X-Ray with Python Powertools

This X-Ray sample demonstrates how to instrument a Python Lambda function with the [AWS Powertools Tracer](https://docs.powertools.aws.dev/lambda/python/latest/core/tracer/)
and shows how to use the X-Ray API to fetch distributed trace data.

## Prerequisites

- LocalStack
- Docker
- `make`
- [awslocal](https://github.com/localstack/awscli-local)
- [samlocal](https://github.com/localstack/aws-sam-cli-local)
- Python / `pip`

## Start LocalStack

Start your LocalStack with your API key configured along with the `DEBUG=1` configuration:

```bash
LOCALSTACK_API_KEY=$LOCALSTACK_API_KEY DEBUG=1 localstack start
```

## Deploy

`make deploy`

The deployment should succeed with the message `Successfully created/updated stack - sam-tracer-lambda in us-east-1`

## Invoke

`make invoke`

The output will print the Lambda invocation logs

```log
Invoking Lambda Function CaptureLambdaHandlerExample                                                                                                                                       
START RequestId: 747a4f9b-c61c-478c-8929-f1850e975030 Version: $LATEST
END RequestId: 747a4f9b-c61c-478c-8929-f1850e975030
REPORT RequestId: 747a4f9b-c61c-478c-8929-f1850e975030  Duration: 9.87 ms       Billed Duration: 10 ms  Memory Size: 128 MB     Max Memory Used: 128 MB
"dummy payment collected for charge: 123"
```

## Get Trace Summaries

`make get-trace-summaries`

The response contains a log entry for every request and includes the `trace_id`.

```log
XRay Event at (2023-09-13T17:14:37.677505) with id (1-6501d1dd-f0f0b7df561e62212e0619b2) and duration (0.000s)
 - 0.000s - ## lambda_handler
```

## Get Traces

`make get-traces`

The response contains the top-level element `Traces` with a list of `Trace` objects for each request.
Each `Trace` contains a collection of segment documents (under `Segments`), which are double JSON-encoded.

```json
{
    "Traces": [
        {
            "Id": "1-6501d1dd-f0f0b7df561e62212e0619b2",
            "Duration": 0,
            "Segments": [
                {
                    "Id": "0e2a8978a948e3ad",
                    "Document": "{\"id\": \"0e2a8978a948e3ad\", \"name\": \"## lambda_handler\", \"start_time\": 1694618077.6775048, \"parent_id\": \"4559ea33aa4a38b0\", \"in_progress\": false, \"annotations\": {\"ColdStart\": true, \"Service\": \"payment\"}, \"metadata\": {\"payment\": {\"lambda_handler response\": \"dummy payment collected for charge: 123\"}}, \"trace_id\": \"1-6501d1dd-f0f0b7df561e62212e0619b2\", \"type\": \"subsegment\", \"namespace\": \"local\", \"end_time\": 1694618077.6775641}"
                }
            ]
        }
    ],
    "UnprocessedTraceIds": []
}
```

## Credits

This sample is based on the [tracer](https://github.com/aws-powertools/powertools-lambda-python/tree/develop/examples/tracer) example from `powertools-lambda-python`.

## License

MIT No Attribution
