# Hot Reloading your Typescript Lambda with LocalStack & Webpack

This is a simple example of how to hot reload your Typescript Lambda with Webpack with the help of LocalStack's Hot Reloading feature.

## Pre-requisites

* [LocalStack](https://docs.localstack.cloud/getting-started/installation)
* [Docker](https://docs.docker.com/get-docker/)
* [Node.js](https://nodejs.org/en/download/)
* [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
* [`awslocal`](https://github.com/localstack/awscli-local)
* [yarn](https://classic.yarnpkg.com/en/docs/install)
* `jq`

## Start LocalStack

Start your LocalStack Docker container with the following command:

```bash
localstack start
```

## Install dependencies

Install the dependencies with the following command:

```bash
yarn install
```

## Build the Lambda

Build the Lambda with the following command:

```bash
npm run build
```

Note that the `build` script is using Nodemon to watch for changes in the `src` directory and rebuild the Lambda. This would be useful when you are developing & testing your Lambda, while making changes to the code in real-time.

With every change, you will see the following output:

```bash
yarn run build
yarn run v1.22.19
$ yarn run clean && yarn run webpack --watch
$ rimraf dist/*
$ cross-env TS_NODE_PROJECT="tsconfig.webpack.json" webpack --mode production --watch
asset api.js 1.4 KiB [emitted] [minimized] (name: api)
./src/api.ts 1.42 KiB [built] [code generated]
./src/util.ts 314 bytes [built] [code generated]
webpack 5.75.0 compiled successfully in 602 ms
[nodemon] 3.0.1
[nodemon] to restart at any time, enter `rs`
[nodemon] watching path(s): dist/api.js
[nodemon] watching extensions: js,mjs,cjs,json
[nodemon] starting `node dist/api.js`
[nodemon] clean exit - waiting for changes before restart
asset api.js 1.4 KiB [emitted] [minimized] (name: api)
./src/api.ts 1.42 KiB [built] [code generated]
./src/util.ts 314 bytes [built] [code generated]
webpack 5.75.0 compiled successfully in 455 ms
[nodemon] restarting due to changes...
[nodemon] starting `node dist/api.js`
```

## Deploy the Lambda

Deploy the Lambda with the following command:

```bash
awslocal lambda create-function \
    --function-name localstack-example \
    --runtime nodejs18.x \
    --role arn:aws:iam::000000000000:role/lambda-ex \
    --code S3Bucket="hot-reload",S3Key="$(PWD)/dist" \
    --handler api.default
```

Additionally, you can create a Lambda Function URL with the following command:

```bash
function_url=$(awslocal lambda create-function-url-config --function-name localstack-example --auth-type NONE | jq -r '.FunctionUrl')
```

## Test the Lambda

You can test the Lambda by sending `POST` requests to the Lambda Function URL:

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"name": "John", "age": 30}' \
  "$function_url"
```

The following output would be displayed:

```bash
{"payload":{"name":"John","age":30}}                                                                         
```

You can additionally test the Lambda with the following command:

```bash
curl -X GET "$function_url"
```

This will return the following output:

```bash
{"error":"Only JSON payload is accepted"}
```

## Hot Reload the Lambda

Go to the `src` directory and make changes to the `api.ts` file. For example, change the following line:

```typescript
return errorResponse("Only JSON payloads are accepted", 406);
```

Make the `errorResponse` function return `"Only JSON payload is accepted"` instead of `"Only JSON payloads are accepted"`. Save the file and run the last `curl` command again:

```bash
curl -X GET "$function_url"
```

This will return the following output:

```bash
{"error":"Only JSON payload is accepted"}
```

You can perform further changes to the `api.ts` file and test the Lambda in real-time.

## How does it work?

The Lambda Hot Reloading feature in LocalStack allows you to hot reload your Lambda code in real-time. In this sample, this is achieved using the following:

- The `build` script in the `package.json` file uses Nodemon to watch for changes in the `src` directory and rebuild the Lambda. This is enabled using the [`nodemon-webpack-plugin`](https://www.npmjs.com/package/nodemon-webpack-plugin) plugin, which has been pre-configured in the `webpack.config.js` file.
- The `S3Bucket` and `S3Key` parameters in the `awslocal lambda create-function` command are used to deploy the Lambda code from the `dist` directory. This is done by specifying the `dist` directory as the `S3Key` parameter. Everytime the Lambda is updated, Nodemon triggers another build and the `dist` directory is updated with the latest code changes. LocalStack then automatically updates the Lambda code with the latest changes from the `dist` directory.

## Notes

This sample application is inherited from a [public repository](https://github.com/pdlug/lambda-typescript-webpack).
