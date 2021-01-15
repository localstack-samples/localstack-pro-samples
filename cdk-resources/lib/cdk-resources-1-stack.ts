import * as path from 'path';
import * as appsync from "@aws-cdk/aws-appsync";
import * as cdk from "@aws-cdk/core";
import * as cognito from "@aws-cdk/aws-cognito";
import * as dynamodb from "@aws-cdk/aws-dynamodb";
import * as events from "@aws-cdk/aws-events";
import * as iam from "@aws-cdk/aws-iam";
import * as lambda from "@aws-cdk/aws-lambda";
import * as lambdaEventSources from "@aws-cdk/aws-lambda-event-sources";
import * as lambdaNodeJs from "@aws-cdk/aws-lambda-nodejs";
import * as secretsmanager from "@aws-cdk/aws-secretsmanager";
import * as sns from "@aws-cdk/aws-sns";
import * as sqs from "@aws-cdk/aws-sqs";
import * as subscriptions from "@aws-cdk/aws-sns-subscriptions";
import * as targets from "@aws-cdk/aws-events-targets";


export class CdkResources1Stack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const queue = new sqs.Queue(this, 'Queue1', {
      visibilityTimeout: cdk.Duration.seconds(300)
    });

    const topic = new sns.Topic(this, 'Topic1');

    topic.addSubscription(new subscriptions.SqsSubscription(queue));

    // // Creates the AppSync API
    // const api = new appsync.GraphqlApi(this, 'Api', {
    //   name: 'cdk-notes-appsync-api',
    //   schema: appsync.Schema.fromAsset('graphql/schema.graphql'),
    //   authorizationConfig: {
    //     defaultAuthorization: {
    //       authorizationType: appsync.AuthorizationType.API_KEY,
    //       apiKeyConfig: {
    //         expires: cdk.Expiration.after(cdk.Duration.days(365))
    //       }
    //     },
    //   },
    //   xrayEnabled: true,
    // });
    //
    // new cdk.CfnOutput(this, "GraphQLAPIURL", {
    //  value: api.graphqlUrl
    // });
    // new cdk.CfnOutput(this, "GraphQLAPIKey", {
    //   value: api.apiKey || ''
    // });
    // new cdk.CfnOutput(this, "Stack Region", {
    //   value: this.region
    // });
    //

    // const layer = new lambda.Function(this, "MyFunction",
    //   runtime=lambda.Runtime.NODEJS_10_X,
    //   handler="index.handler",
    //   code=lambda.Code.fromAsset(path.join(__dirname, "lambda-handler"))
    // );

    const layer = new lambda.LayerVersion(this, 'Layer1', {
      code: lambda.Code.fromAsset(path.join(__dirname, '../lambda/layer1')),
      compatibleRuntimes: [lambda.Runtime.NODEJS_10_X, lambda.Runtime.NODEJS_12_X]
    });

    const myLambda = new lambda.Function(this, 'Func1', {
      runtime: lambda.Runtime.NODEJS_12_X,
      handler: 'main.handler',
      code: lambda.Code.fromAsset('lambda/func1'),
      memorySize: 1024,
      layers: [layer]
    });

    const eventSource = myLambda.addEventSource(new lambdaEventSources.SqsEventSource(queue));

    // Set the new Lambda function as a data source for the AppSync API
    // const lambdaDs = api.addLambdaDataSource('lambdaDatasource', notesLambda);

    // lambdaDs.createResolver({
    //   typeName: "Query",
    //   fieldName: "getNoteById"
    // });
    //
    // lambdaDs.createResolver({
    //   typeName: "Query",
    //   fieldName: "listNotes"
    // });
    //
    // lambdaDs.createResolver({
    //   typeName: "Mutation",
    //   fieldName: "createNote"
    // });
    //
    // lambdaDs.createResolver({
    //   typeName: "Mutation",
    //   fieldName: "deleteNote"
    // });
    //
    // lambdaDs.createResolver({
    //   typeName: "Mutation",
    //   fieldName: "updateNote"
    // });

    const tableName = 'items'

    const itemsGraphQLApi = new appsync.CfnGraphQLApi(this, 'ItemsApi', {
      name: 'items-api',
      authenticationType: 'API_KEY'
    });

    new appsync.CfnApiKey(this, 'ItemsApiKey', {
      apiId: itemsGraphQLApi.attrApiId
    });

    const apiSchema = new appsync.CfnGraphQLSchema(this, 'ItemsSchema', {
      apiId: itemsGraphQLApi.attrApiId,
      definition: `type ${tableName} {
        ${tableName}Id: ID!
        name: String
      }
      type Paginated${tableName} {
        items: [${tableName}!]!
        nextToken: String
      }
      type Query {
        all(limit: Int, nextToken: String): Paginated${tableName}!
        getOne(${tableName}Id: ID!): ${tableName}
      }
      type Mutation {
        save(name: String!): ${tableName}
        delete(${tableName}Id: ID!): ${tableName}
      }
      type Schema {
        query: Query
        mutation: Mutation
      }`
    });

    const itemsTable = new dynamodb.Table(this, 'ItemsTable', {
      tableName: tableName,
      partitionKey: {
        name: `${tableName}Id`,
        type: dynamodb.AttributeType.STRING
      },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
      stream: dynamodb.StreamViewType.NEW_IMAGE,

      // The default removal policy is RETAIN, which means that cdk destroy will not attempt to delete
      // the new table, and it will remain in your account until manually deleted. By setting the policy to
      // DESTROY, cdk destroy will delete the table (even if it has data in it)
      removalPolicy: cdk.RemovalPolicy.DESTROY, // NOT recommended for production code
    });

    const itemsTableRole = new iam.Role(this, 'ItemsDynamoDBRole', {
      assumedBy: new iam.ServicePrincipal('appsync.amazonaws.com')
    });

    itemsTableRole.addManagedPolicy(iam.ManagedPolicy.fromAwsManagedPolicyName('AmazonDynamoDBFullAccess'));

    const dataSource = new appsync.CfnDataSource(this, 'ItemsDataSource', {
      apiId: itemsGraphQLApi.attrApiId,
      name: 'ItemsDynamoDataSource',
      type: 'AMAZON_DYNAMODB',
      dynamoDbConfig: {
        tableName: itemsTable.tableName,
        awsRegion: this.region
      },
      serviceRoleArn: itemsTableRole.roleArn
    });

    const getOneResolver = new appsync.CfnResolver(this, 'GetOneQueryResolver', {
      apiId: itemsGraphQLApi.attrApiId,
      typeName: 'Query',
      fieldName: 'getOne',
      dataSourceName: dataSource.name,
      requestMappingTemplate: `{
        "version": "2017-02-28",
        "operation": "GetItem",
        "key": {
          "${tableName}Id": $util.dynamodb.toDynamoDBJson($ctx.args.${tableName}Id)
        }
      }`,
      responseMappingTemplate: `$util.toJson($ctx.result)`
    });
    getOneResolver.addDependsOn(apiSchema);

    const getAllResolver = new appsync.CfnResolver(this, 'GetAllQueryResolver', {
      apiId: itemsGraphQLApi.attrApiId,
      typeName: 'Query',
      fieldName: 'all',
      dataSourceName: dataSource.name,
      requestMappingTemplate: `{
        "version": "2017-02-28",
        "operation": "Scan",
        "limit": $util.defaultIfNull($ctx.args.limit, 20),
        "nextToken": $util.toJson($util.defaultIfNullOrEmpty($ctx.args.nextToken, null))
      }`,
      responseMappingTemplate: `$util.toJson($ctx.result)`
    });
    getAllResolver.addDependsOn(apiSchema);

    const saveResolver = new appsync.CfnResolver(this, 'SaveMutationResolver', {
      apiId: itemsGraphQLApi.attrApiId,
      typeName: 'Mutation',
      fieldName: 'save',
      dataSourceName: dataSource.name,
      requestMappingTemplate: `{
        "version": "2017-02-28",
        "operation": "PutItem",
        "key": {
          "${tableName}Id": { "S": "$util.autoId()" }
        },
        "attributeValues": {
          "name": $util.dynamodb.toDynamoDBJson($ctx.args.name)
        }
      }`,
      responseMappingTemplate: `$util.toJson($ctx.result)`
    });
    saveResolver.addDependsOn(apiSchema);

    const deleteResolver = new appsync.CfnResolver(this, 'DeleteMutationResolver', {
      apiId: itemsGraphQLApi.attrApiId,
      typeName: 'Mutation',
      fieldName: 'delete',
      dataSourceName: dataSource.name,
      requestMappingTemplate: `{
        "version": "2017-02-28",
        "operation": "DeleteItem",
        "key": {
          "${tableName}Id": $util.dynamodb.toDynamoDBJson($ctx.args.${tableName}Id)
        }
      }`,
      responseMappingTemplate: `$util.toJson($ctx.result)`
    });

    deleteResolver.addDependsOn(apiSchema);
  }
}
