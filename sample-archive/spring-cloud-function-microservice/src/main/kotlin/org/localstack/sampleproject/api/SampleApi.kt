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

package org.localstack.sampleproject.api

import com.fasterxml.jackson.databind.ObjectMapper
import org.localstack.sampleproject.model.SampleModel
import org.localstack.sampleproject.util.Logger
import org.localstack.sampleproject.util.apiGatewayFunction
import org.localstack.sampleproject.util.buildJsonResponse
import org.springframework.context.annotation.Bean
import org.springframework.stereotype.Component


private val SAMPLE_RESPONSE = mutableListOf(
    SampleModel(id = 1, name = "Sample #1"),
    SampleModel(id = 2, name = "Sample #2"),
)


@Component
class SampleApi(private val objectMapper: ObjectMapper) {

    companion object : Logger()

    @Bean("POST /v1/entities")
    fun createSampleEntity() = apiGatewayFunction<SampleModel>(objectMapper) { input, context ->
        LOGGER.info("calling POST /v1/entities")
        SAMPLE_RESPONSE.add(input.payload)
        buildJsonResponse(input.payload, code = 201)
    }

    @Bean("GET /v1/entities")
    fun listSampleEntities() = apiGatewayFunction<ByteArray>(objectMapper) { input, context ->
        LOGGER.info("calling GET /v1/entities")
        buildJsonResponse(SAMPLE_RESPONSE)
    }

    @Bean("GET /v1/entities/get")
    fun getSampleEntity() = apiGatewayFunction<ByteArray>(objectMapper) { input, context ->
        LOGGER.info("calling GET /v1/entities/get")
        val desiredId = context.queryStringParameters["id"]!!.toInt()
        buildJsonResponse(SAMPLE_RESPONSE.find { it.id == desiredId })
    }
}
