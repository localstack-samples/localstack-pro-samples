import { CfnOutput, Stack, StackProps } from "aws-cdk-lib";
import { Construct } from "constructs";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as apigateway from "@aws-cdk/aws-apigatewayv2-alpha";
import { HttpLambdaIntegration } from "@aws-cdk/aws-apigatewayv2-integrations-alpha";

// AWS CDK Bref example based on https://gist.github.com/s0enke/499af16f0e2f049c1d58f6b6c045005f
export class PhpBrefStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    // Using non-fpm layer for "HTTP handler class" here.
    // See Bref docs for traditional "Bref for web apps" runtime using "fpm":
    // https://bref.sh/docs/function/handlers.html#api-gateway-http-events
    const region = Stack.of(this).region
    const brefLayer = lambda.LayerVersion.fromLayerVersionArn(
      this,
      "php-82",
      // https://runtimes.bref.sh/?region=us-east-1&version=1.7.16
      `arn:aws:lambda:${region}:209497400698:layer:php-82:16`
    )
    const handler = new lambda.Function(this, "PhpRuntime", {
      runtime: lambda.Runtime.PROVIDED_AL2,
      handler: "index.php",
      code: lambda.Code.fromAsset("./backend"),
      memorySize: 1024,
      layers: [brefLayer],
    });

    const api = new apigateway.HttpApi(this, "HttpApi");

    const lambdaHandlerIntegration = new HttpLambdaIntegration(
      "Integration",
      handler
    );

    api.addRoutes({
      path: "/",
      methods: [apigateway.HttpMethod.GET],
      integration: lambdaHandlerIntegration,
    });

    new CfnOutput(this, "Url", {
      value: api.url!,
    });
  }
}
