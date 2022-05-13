package cloud.localstack.demos.gluemsk.producer;

import cloud.localstack.demos.gluemsk.schema.*;
import com.amazonaws.services.schemaregistry.serializers.GlueSchemaRegistryKafkaSerializer;
import com.amazonaws.services.schemaregistry.utils.AWSSchemaRegistryConstants;
import com.amazonaws.services.schemaregistry.utils.AvroRecordType;
import com.beust.jcommander.JCommander;
import com.beust.jcommander.Parameter;
import org.apache.kafka.clients.producer.*;
import org.apache.kafka.common.serialization.StringSerializer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import software.amazon.awssdk.services.glue.model.DataFormat;

import java.util.List;
import java.util.Properties;

public class Producer {
    private final static Logger LOGGER = LoggerFactory.getLogger(org.apache.kafka.clients.producer.Producer.class.getName());

    @Parameter(names = {"--help", "-h"}, help = true)
    protected boolean help = false;
    @Parameter(names = {"--bootstrap-servers", "-bs"}, description = "Kafka bootstrap servers endpoint to connect to.")
    protected String bootstrapServers = "localhost:4511";
    @Parameter(names = {"--aws-endpoint-servers", "-ae"}, description = "AWS endpoint to use.")
    protected String awsEndpoint = "https://localhost.localstack.cloud:4566";
    @Parameter(names = {"--region", "-reg"}, description = "AWS Region to use.")
    protected String regionName = "us-east-1";
    @Parameter(names = {"--topic-name", "-topic"}, description = "Kafka topic name where you send the data records. Default is unicorn-ride-request-topic.")
    protected String topic = "unicorn-ride-request-topic";
    @Parameter(names = {"--num-messages", "-nm"}, description = "Number of messages you want producer to send. Default is 100.")
    protected String str_numOfMessages = "100";


    public static void main(String[] args) {
        Producer producer = new Producer();
        JCommander jc = JCommander.newBuilder().addObject(producer).build();
        jc.parse(args);
        if (producer.help) {
            jc.usage();
            return;
        }
        producer.startProducer();
    }

    public void startProducer() {
        try (KafkaProducer<String, UnicornRideRequest> producer = new KafkaProducer<>(getProducerConfig())) {
            int numberOfMessages = Integer.parseInt(str_numOfMessages);
            LOGGER.info("Starting to send records...");
            for (int i = 0; i < numberOfMessages; i++) {
                UnicornRideRequest rideRequest = getRecord(i);
                String key = "key-" + i;
                ProducerRecord<String, UnicornRideRequest> record = new ProducerRecord<>(topic, key, rideRequest);
                producer.send(record, new ProducerCallback());
            }
        }
    }

    public UnicornRideRequest getRecord(int requestId) {
            /*
             Initialise UnicornRideRequest object of
             class that is generated from AVRO Schema
             */
        UnicornRideRequest rideRequest = UnicornRideRequest.newBuilder()
                .setRequestId(requestId)
                .setPickupAddress("Melbourne, Victoria, Australia")
                .setDestinationAddress("Sydney, NSW, Aus")
                .setRideFare(1200.50F)
                .setRideDuration(120)
                .setPreferredUnicornColor(UnicornPreferredColor.WHITE)
                .setRecommendedUnicorn(RecommendedUnicorn.newBuilder()
                        .setUnicornId(requestId * 2)
                        .setColor(unicorn_color.WHITE)
                        .setStarsRating(5).build())
                .setCustomer(Customer.newBuilder()
                        .setCustomerAccountNo(1001)
                        .setFirstName("Dummy")
                        .setLastName("User")
                        .setEmailAddresses(List.of("demo@example.com"))
                        .setCustomerAddress("Flinders Street Station")
                        .setModeOfPayment(ModeOfPayment.CARD)
                        .setCustomerRating(5).build()).build();
        LOGGER.info(rideRequest.toString());
        return rideRequest;
    }

    private Properties getProducerConfig() {
        Properties props = new Properties();
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, this.bootstrapServers);
        props.put(ProducerConfig.ACKS_CONFIG, "-1");
        props.put(ProducerConfig.CLIENT_ID_CONFIG, "glue-msk-demo-producer");
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, GlueSchemaRegistryKafkaSerializer.class.getName());
        props.put(AWSSchemaRegistryConstants.DATA_FORMAT, DataFormat.AVRO.name());
        props.put(AWSSchemaRegistryConstants.AWS_REGION, regionName);
        props.put(AWSSchemaRegistryConstants.REGISTRY_NAME, "unicorn-ride-request-registry");
        props.put(AWSSchemaRegistryConstants.SCHEMA_NAME, "unicorn-ride-request-schema-avro");
        props.put(AWSSchemaRegistryConstants.AVRO_RECORD_TYPE, AvroRecordType.SPECIFIC_RECORD.getName());
        props.put(AWSSchemaRegistryConstants.AWS_ENDPOINT, this.awsEndpoint);
        // Enable compression of records
        props.put(AWSSchemaRegistryConstants.COMPRESSION_TYPE, AWSSchemaRegistryConstants.COMPRESSION.ZLIB.name());
        return props;
    }

    private static class ProducerCallback implements Callback {
        @Override
        public void onCompletion(RecordMetadata recordMetaData, Exception e) {
            if (e == null) {
                LOGGER.info("Received new metadata. \t" +
                        "Topic:" + recordMetaData.topic() + "\t" +
                        "Partition: " + recordMetaData.partition() + "\t" +
                        "Offset: " + recordMetaData.offset() + "\t" +
                        "Timestamp: " + recordMetaData.timestamp());
            } else {
                LOGGER.info("There's been an error from the Producer side");
                e.printStackTrace();
            }
        }
    }
}