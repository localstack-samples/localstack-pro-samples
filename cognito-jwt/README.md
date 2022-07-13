# LocalStack Demo: Cognito Auth with Email Verification

Simple demo application illustrating Cognito authentication and user pools running locally using LocalStack.

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

## Starting LocalStack

This scenario requires access to an SMTP server to send Cognito emails (e.g., to send codes for account activation). Please make sure the following environment variables are configured properly:
* `SMTP_HOST`: SMTP host
* `SMTP_USER`: SMTP username
* `SMTP_PASS`: SMTP password
* `SMTP_EMAIL`: Email address under which the messages should be sent

Make sure that LocalStack is started:
```
LOCALSTACK_API_KEY=... DEBUG=1 localstack start
```

## Running

Please make sure to configure the environment variable `$USER_EMAIL` with an email address that can be used to send account activation emails.

Run the scenario script with the Cognito commands as follows:
```
make run
```

You should see some log outputs from the script. At some point, the script will ask you to enter the confirmation code that has been sent to your email address (note: the code is also printed in the LocalStack terminal):
```
Please check email inbox for ..., and enter the confirmation code below:
```

The script will then also ask you to specify a password reset code that is sent to your email (and also printed in the LocalStack terminal):
```
Please check email inbox for ..., and enter the password reset code here:
```

## Credits

* Kudos to `@Jaystified`, [Kurusugawa Computer Inc.](https://kurusugawa.jp) who kindly provided the initial version of the testing script in `test.sh`.

## License

This code is available under the Apache 2.0 license.
