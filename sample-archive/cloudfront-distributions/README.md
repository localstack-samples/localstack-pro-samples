# LocalStack Demo: Serving Files and APIs via CloudFront

Simple demo application illustrating CloudFront distributions running locally using LocalStack.

## Prerequisites

* LocalStack
* Docker
* `make`
* [`awslocal`](https://github.com/localstack/awscli-local)

## Installing

To install the dependencies:
```
make install
```

## App Details

Please refer to the `distconfig.json` file for details about the CloudFront distribution.

## Starting LocalStack

Make sure that LocalStack is started with the following `SERVICES` configuration:
```
LOCALSTACK_API_KEY=... DEBUG=1 SERVICES=edge,serverless,ssm,cloudfront localstack start
```

Please also ensure that your local IP address is registered as a DNS nameserver in your environment (e.g., by configuring `/etc/resolv.conf`).

## Running

Deploy the app locally and run a Lambda test invocation:
```
make run
```

You should see some log output of the Serverless deployment, then a success message in the terminal:
```
Serverless: Stack update finished...
...
Trying to call distribution endpoint (note: it may take a few minutes for the DNS name to become available)
curl -k https://69e6db0c.cloudfront.net/index
...
<html>
<body>
...
```

Finally, the test app should be accessible under the URL from the output above, e.g., https://69e6db0c.cloudfront.net/index .

Please note: It may take some time for the DNS name to propagate and become available in your environment - you may have to retry loading the page in your browser a couple of times.

## License

This code is available under the Apache 2.0 license.
