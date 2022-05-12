package com.example;

import java.net.URI;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import software.amazon.awssdk.auth.credentials.EnvironmentVariableCredentialsProvider;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.ses.SesClient;
import software.amazon.awssdk.services.sqs.SqsClient;

@Configuration
public class AwsConfiguration {

    private static final String ENDPOINT_URL = "http://localhost:4566";


    private static final Region DEFAULT_REGION = Region.US_EAST_1;

    @Bean
    public SqsClient sqsClient() {
        return SqsClient.builder()
                .region(DEFAULT_REGION)
                .credentialsProvider(EnvironmentVariableCredentialsProvider.create())
                .applyMutation(builder -> {
                    // TODO: conditional local-dev injection
                    builder.endpointOverride(URI.create(ENDPOINT_URL));
                })
                .build();
    }

    @Bean
    public SesClient sesClient() {
        return SesClient.builder()
                .region(DEFAULT_REGION)
                .credentialsProvider(EnvironmentVariableCredentialsProvider.create())
                .applyMutation(builder -> {
                    // TODO: conditional local-dev injection
                    builder.endpointOverride(URI.create(ENDPOINT_URL));
                })
                .build();
    }

    @Bean
    @Autowired
    public String notificationQueueUrl(SqsClient sqsClient) {
        return sqsClient.getQueueUrl(builder -> {
            // TODO: could get QueueUrl from stack output properties
            builder.queueName("email-notification-queue");
        }).queueUrl();
    }
}
