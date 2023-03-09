/*
 * Copyright (c) 2017-2021 LocalStack maintainers and contributors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.localstack.cdkstack

import java.util.UUID
import software.amazon.awscdk.core.Construct
import software.amazon.awscdk.core.Duration
import software.amazon.awscdk.core.Stack
import software.amazon.awscdk.services.apigateway.CorsOptions
import software.amazon.awscdk.services.apigateway.LambdaRestApi
import software.amazon.awscdk.services.apigateway.StageOptions
import software.amazon.awscdk.services.events.Rule
import software.amazon.awscdk.services.events.RuleTargetInput
import software.amazon.awscdk.services.events.Schedule
import software.amazon.awscdk.services.events.targets.LambdaFunction
import software.amazon.awscdk.services.lambda.*
import software.amazon.awscdk.services.lambda.Function
import software.amazon.awscdk.services.s3.Bucket

private val STAGE = System.getenv("STAGE") ?: "local"
private val LAMBDA_MOUNT_CWD = System.getenv("LAMBDA_MOUNT_CWD") ?: ""
private const val JAR_PATH = "../../build/libs/localstack-sampleproject-all.jar"

class ApplicationStack(parent: Construct, name: String) : Stack(parent, name) {

    init {
        val lambdaCodeSource = this.buildCodeSource()

        val restApiLambda = Function.Builder.create(this, "RestApiFunction")
            .code(lambdaCodeSource)
            .handler("org.springframework.cloud.function.adapter.aws.FunctionInvoker")
            .timeout(Duration.seconds(30))
            .runtime(Runtime.JAVA_11)
            .tracing(Tracing.ACTIVE)
            .build()

        val corsOptions = CorsOptions.builder().allowOrigins(listOf("*")).allowMethods(listOf("*")).build()

        LambdaRestApi.Builder.create(this, "ExampleRestApi")
            .proxy(true)
            .restApiName("ExampleRestApi")
            .defaultCorsPreflightOptions(corsOptions)
            .deployOptions(StageOptions.Builder().stageName(STAGE).build())
            .handler(restApiLambda)
            .build()

        val warmupRule = Rule.Builder.create(this, "WarmupRule")
            .schedule(Schedule.rate(Duration.minutes(10)))
            .build()

        val warmupTarget = LambdaFunction.Builder.create(restApiLambda)
            .event(RuleTargetInput.fromObject(mapOf("httpMethod" to "SCHEDULE", "path" to "warmup")))
            .build()

        // Please note that events is a LocalStack PRO feature
        warmupRule.addTarget(warmupTarget)

        SingletonFunction.Builder.create(this, "ExampleFunctionOne")
            .code(lambdaCodeSource)
            .handler("org.localstack.sampleproject.api.LambdaApi")
            .environment(mapOf("FUNCTION_NAME" to "functionOne"))
            .timeout(Duration.seconds(30))
            .runtime(Runtime.JAVA_11)
            .uuid(UUID.randomUUID().toString())
            .build()

        SingletonFunction.Builder.create(this, "ExampleFunctionTwo")
            .code(lambdaCodeSource)
            .handler("org.localstack.sampleproject.api.LambdaApi")
            .environment(mapOf("FUNCTION_NAME" to "functionTwo"))
            .timeout(Duration.seconds(30))
            .runtime(Runtime.JAVA_11)
            .uuid(UUID.randomUUID().toString())
            .build()
    }

    /**
     * Mount code for hot-reloading when STAGE=local
     */
    private fun buildCodeSource(): Code  {
        if (STAGE == "local") {
            val bucket = Bucket.fromBucketName(this, "HotReloadingBucket", "hot-reload")
            return Code.fromBucket(bucket, LAMBDA_MOUNT_CWD)
        }

        return Code.fromAsset(JAR_PATH)
    }
}
