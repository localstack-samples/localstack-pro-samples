# LocalStack Demo: API Gateway with Custom Domains

Simple demo application illustrating API Gateway (v2) endpoints using custom domain names (via Route53, ACM), deployed locally in LocalStack using the Serverless framework.

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

Make sure that LocalStack is started:
```
LOCALSTACK_API_KEY=... DEBUG=1 localstack start
```

Deploy the app locally and run a test invocation via:
```
make run
```

The script first generates an SSL certificate for local testing (in case the `openssl` command is not available, it will use an existing, predefined certificate), and then adds it to Amazon Certificate Manager (ACM), and finally creates a Route53 hosted zone for the domain name `test.example.com`:
```
Generating a 2048 bit RSA private key
...
subject=/CN=test.example.com
...
Importing local test certificate into ACM API ...
{
    "CertificateArn": "arn:aws:acm:us-east-1:000000000000:certificate/9cbc69d6-abf9-412e-9e2b-36f99fcbf251"
}
Creating Route53 hosted zone for test domain 'test.example.com' ...
{
    "HostedZone": {
        "Id": "/hostedzone/SU1TPRNX6CL3OE0",
        "Name": "test.example.com.",
        ...
```

Next, you should see some output with the deployment logs of the Serverless application, and some details in the output section towards the bottom:
```
...
Serverless Domain Manager: Info: Created API mapping '(none)' for test.example.com
Serverless Domain Manager: Summary: Distribution Domain Name
Serverless Domain Manager:    Domain Name: test.example.com
Serverless Domain Manager:    Target Domain: test.example.com
Serverless Domain Manager:    Hosted Zone Id: Z2FDTNDATAQYW2
```

Finally, the script runs two invocations of the new API GW API deployed under the custom domain name `test.example.com`:
```
Invoking endpoint 1: http://test.example.com:4566/hello
...

Invoking endpoint 2: http://test.example.com:4566/goodbye
...
```

## License

This code is available under the Apache 2.0 license.
