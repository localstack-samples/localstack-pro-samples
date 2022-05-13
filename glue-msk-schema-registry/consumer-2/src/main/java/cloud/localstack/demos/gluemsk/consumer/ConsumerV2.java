package cloud.localstack.demos.gluemsk.consumer;

import cloud.localstack.demos.gluemsk.schema.UnicornRideRequest;
import com.amazonaws.services.schemaregistry.deserializers.GlueSchemaRegistryKafkaDeserializer;
import com.amazonaws.services.schemaregistry.utils.AWSSchemaRegistryConstants;
import com.amazonaws.services.schemaregistry.utils.AvroRecordType;
import com.beust.jcommander.JCommander;
import com.beust.jcommander.Parameter;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.time.Duration;
import java.util.Collections;
import java.util.Properties;

public class ConsumerV2 {
    private final static Logger LOGGER = LoggerFactory.getLogger(java.util.function.Consumer.class.getName());

    @Parameter(names = {"--help", "-h"}, help = true)
    protected boolean help = false;
    @Parameter(names = {"--bootstrap-servers", "-bs"}, description = "kafka bootstrap servers endpoint")
    protected String bootstrapServers = "localhost:4511";
    @Parameter(names = {"--aws-endpoint-servers", "-ae"}, description = "AWS endpoint")
    protected String awsEndpoint = "https://localhost.localstack.cloud:4566";
    @Parameter(names = {"--region", "-reg"}, description = "AWS Region to use.")
    protected String regionName = "us-east-1";
    @Parameter(names = {"--topic-name", "-topic"}, description = "Kafka topic name where you send the data records. Default is unicorn-ride-request-topic")
    protected String topic = "unicorn-ride-request-topic";
    @Parameter(names = {"--num-messages", "-nm"}, description = "Number of messages you want consumer to wait for until it stops. Default is 100, use 0 if you want it to run indefinitely.")
    protected String str_numOfMessages = "100";


    public static void main(String[] args) {
        ConsumerV2 consumer = new ConsumerV2();
        JCommander jc = JCommander.newBuilder().addObject(consumer).build();
        jc.parse(args);
        if (consumer.help) {
            jc.usage();
            return;
        }
        consumer.startConsumer();
    }

    public void startConsumer() {
        LOGGER.info("Starting consumer...");
        try (KafkaConsumer<String, UnicornRideRequest> consumer = new KafkaConsumer<>(getConsumerConfig())) {
            consumer.subscribe(Collections.singletonList(topic));
            int outstandingMessages = Integer.parseInt(str_numOfMessages);
            boolean runIndefinitely = outstandingMessages == 0;
            while (outstandingMessages > 0 || runIndefinitely) {
                // a real consumer would probably run in an endless loop waiting for new records here
                final ConsumerRecords<String, UnicornRideRequest> records = consumer.poll(Duration.ofMillis(10));
                for (final ConsumerRecord<String, UnicornRideRequest> record : records) {
                    final UnicornRideRequest rideRequest = record.value();
                    LOGGER.info(String.valueOf(rideRequest.getRequestId()));
                    LOGGER.info(rideRequest.toString());
                    outstandingMessages--;
                }
            }
        }
        LOGGER.info("Stopping consumer...");
    }

    private Properties getConsumerConfig() {
        Properties props = new Properties();
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, this.bootstrapServers);
        props.put(ConsumerConfig.GROUP_ID_CONFIG, "unicorn.riderequest.consumer");
        props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, GlueSchemaRegistryKafkaDeserializer.class.getName());
        props.put(AWSSchemaRegistryConstants.AWS_REGION, this.regionName);
        props.put(AWSSchemaRegistryConstants.AVRO_RECORD_TYPE, AvroRecordType.SPECIFIC_RECORD.getName());
        props.put(AWSSchemaRegistryConstants.AWS_ENDPOINT, this.awsEndpoint);
        return props;
    }
}

