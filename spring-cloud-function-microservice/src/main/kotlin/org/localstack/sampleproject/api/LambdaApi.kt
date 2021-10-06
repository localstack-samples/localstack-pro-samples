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

import com.amazonaws.services.lambda.runtime.events.DynamodbEvent
import org.localstack.sampleproject.model.SampleModel
import org.localstack.sampleproject.util.Logger
import org.springframework.cloud.function.adapter.aws.SpringBootStreamHandler
import org.springframework.context.annotation.Bean
import org.springframework.stereotype.Component
import java.util.function.Function

@Component
class LambdaApi : SpringBootStreamHandler() {

    companion object : Logger()

    @Bean
    fun functionOne(): Function<Any, String> {
        return Function {
            LOGGER.info("calling function one")
            return@Function "ONE";
        }
    }

    @Bean
    fun functionTwo(): Function<SampleModel, SampleModel> {
        return Function {
            LOGGER.info("calling function two")
            return@Function it;
        }
    }

    @Bean
    fun dynamoDbStreamHandlerExample(): Function<DynamodbEvent, Unit> {
        return Function {
            LOGGER.info("handling DynamoDB stream event")
        }
    }
}
