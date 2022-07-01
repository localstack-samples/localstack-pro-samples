# Creating Cloudwatch metric alarms

This is a simple example for creating cloudwatch metric alarm.
The example creates an alarm based on the metrics of a failing lambda. 

In other words: once the lambda fails, the alarm will be triggered - in our example we use SNS notification via email.


## Prerequisites

For this example you will need:
* [LocalStack Pro](https://localstack.cloud), to send emails via SMTP and SES.
* The [awslocal](https://docs.localstack.cloud/integrations/aws-cli/#localstack-aws-cli-awslocal) command line utility
* A mock SMTP server like [smtp4dev](https://github.com/rnwood/smtp4dev) or [Papercut SMTP](https://github.com/ChangemakerStudios/Papercut-SMTP) to receive the email notifications locally.

To connect LocalStack with the SMTP server, you need to [configure the following SMTP environment variables](https://docs.localstack.cloud/aws/ses/#pro) when starting LocalStack:
 * `SMTP_HOST` this should contain the hostname and the port of your mock SMTP server
 * `SMTP_USER` optional, if there is user to connect
 * `SMTP_PASS` optional

For example, when using smtp4dev, simply run:

    docker run --rm -it -p 3000:80 -p 2525:25 rnwood/smtp4dev

and set `SMTP_HOST=localhost:2525`.
Navigating to `http://localhost:3000` will open a UI to access the email notifications.

Alternatively, you can use your real smtp server. Please refer to your provider to set the proper values for `SMTP_HOST`, `SMTP_USER` and `SMTP_PASS`
