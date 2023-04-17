# Hot reloading for TypeScript Lambdas

You can hot-reload your [TypeScript Lambda functions](https://docs.aws.amazon.com/lambda/latest/dg/lambda-typescript.html). We will check-out a simple example to create a simple `Hello World!` Lambda function using TypeScript.

## Setting up the Lambda function

Create a new Node.js project with `npm` or an alternative package manager:

```sh
$ npm init -y
```

Install the the [@types/aws-lambda](https://www.npmjs.com/package/@types/aws-lambda) and [esbuild](https://esbuild.github.io/) packages in your Node.js project:

```sh
$ npm install -D @types/aws-lambda esbuild
```

Create a new file named `index.ts`. Add the following code to the new file:

```ts
import { Context, APIGatewayProxyResult, APIGatewayEvent } from 'aws-lambda';
export const handler = async (event: APIGatewayEvent, context: Context): Promise<APIGatewayProxyResult> => {
  console.log(`Event: ${JSON.stringify(event, null, 2)}`);
  console.log(`Context: ${JSON.stringify(context, null, 2)}`);
  return {
      statusCode: 200,
      body: JSON.stringify({
          message: 'Hello World!',
      }),
   };
};
```

Add a build script to your `package.json` file:

```json
"scripts": {
    "build": "esbuild index.ts --bundle --minify --sourcemap --platform=node --target=es2020 --outfile=dist/index.js --watch"
}
```

The build script will use `esbuild` to bundle and minify the TypeScript code into a single JavaScript file, which will be placed in the `dist` folder. The `--watch` flag will make sure that the build script will watch for any changes in the source code and re-build the code.

You can now run the build script to create the `dist/index.js` file:

```sh
$ npm run build
```

## Creating the Lambda Function

To create the Lambda function, you need to take care of two things:

- Deploy via an S3 Bucket. You need to use the magic variable `hot-reload` as the bucket.
- Set the S3 key to the path of the directory your lambda function resides in. The handler is then referenced by the filename of your lambda code and the function in that code that needs to be invoked.

Create the Lambda Function using the `awslocal` CLI:

```sh
awslocal lambda create-function \
    --function-name hello-world \
    --runtime "nodejs16.x" \
    --role arn:aws:iam::123456789012:role/lambda-ex \
    --code S3Bucket="hot-reload",S3Key="${PWD}/dist" \
    --handler index.handler
```

You can quickly make sure that it works by invoking it with a simple payload:

```
$ awslocal lambda invoke \
    --function-name hello-world \
    --payload '{"action": "test"}' output.txt
```

The invocation returns itself returns:

```sh
{
    "StatusCode": 200,
    "ExecutedVersion": "$LATEST"
}
```

The `output.txt` file contains the following:

```sh
{"statusCode":200,"body":"{\"message\":\"Hello World!\"}"}
```

## Changing the Lambda Function

The Lambda function is now mounted as a file in the executing container, hence any change that we save on the file will be there in an instant.

Change the `Hello World!` message to `Hello LocalStack!`, and trigger the Lambda once again. You will see the following in the `output.txt` file:

```sh
{"statusCode":200,"body":"{\"message\":\"Hello LocalStack!\"}"}
```
