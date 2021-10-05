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

package org.localstack.sampleproject.util

import com.amazonaws.services.lambda.runtime.events.APIGatewayProxyRequestEvent
import com.fasterxml.jackson.databind.ObjectMapper
import org.springframework.messaging.Message
import java.util.function.Function

fun <T>apiGatewayFunction(
    objectMapper: ObjectMapper,
    callable: (message: Message<T>, context: APIGatewayProxyRequestEvent) -> Message<*>
): Function<Message<T>, Message<*>> = Function { input ->
    try {
        val context = objectMapper.readValue(
            objectMapper.writeValueAsString(input.headers),
            APIGatewayProxyRequestEvent::class.java
        )

        return@Function callable(input, context)
    } catch (e: Throwable) {
        val message = e.message?.replace("\n", "")?.replace("\"", "'")
        return@Function buildJsonErrorResponse(message ?: "", 500)
    }
}
