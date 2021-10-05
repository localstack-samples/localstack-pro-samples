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

package org.localstack.sampleproject.config

import com.fasterxml.jackson.annotation.JsonInclude
import com.fasterxml.jackson.databind.*
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.context.annotation.Primary
import org.springframework.http.converter.json.Jackson2ObjectMapperBuilder
import java.text.DateFormat

@Configuration
class JacksonConfiguration {

    @Bean
    fun jacksonBuilder() = Jackson2ObjectMapperBuilder()
        .dateFormat(DateFormat.getDateInstance(DateFormat.FULL))

    @Bean
    @Primary
    fun objectMapper(): ObjectMapper = ObjectMapper().apply {
        configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false)
        configure(SerializationFeature.FAIL_ON_EMPTY_BEANS, false)
        configure(SerializationFeature.WRITE_ENUMS_USING_TO_STRING, true)
        configure(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS, false)
        configure(SerializationFeature.ORDER_MAP_ENTRIES_BY_KEYS, true)
        configure(MapperFeature.SORT_PROPERTIES_ALPHABETICALLY, true)
        setSerializationInclusion(JsonInclude.Include.NON_NULL)
        findAndRegisterModules()
    }
}
