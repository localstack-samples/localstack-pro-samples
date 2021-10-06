package org.localstack.sampleproject.api

import cloud.localstack.LocalstackTestRunner
import cloud.localstack.awssdkv2.TestUtils
import junit.framework.TestCase.assertEquals
import org.junit.BeforeClass
import org.junit.Test
import org.junit.runner.RunWith
import software.amazon.awssdk.core.SdkBytes
import software.amazon.awssdk.services.lambda.model.InvocationType
import java.nio.charset.Charset

@RunWith(LocalstackTestRunner::class)
class LambdaApiTest {

    companion object {

        @BeforeClass @JvmStatic fun deployStack() {
            Runtime.getRuntime().exec("make STAGE=testing deploy-sls").waitFor()
        }
    }

    @Test fun testFunctionOneInvocation() {
        val lambda = TestUtils.getClientLambdaAsyncV2()
        val result = lambda.invoke {
            it.payload(SdkBytes.fromString("{}", Charset.forName("UTF-8")))
            it.invocationType(InvocationType.REQUEST_RESPONSE)
            it.functionName("localstack-sampleproject-serverless-testing-lambda_helloOne")
        }.get()

        assertEquals(result.payload().asUtf8String(), "\"ONE\"\n")
    }
}
