import com.amazonaws.AmazonServiceException;
import com.amazonaws.auth.AWSCredentials;
import com.amazonaws.auth.BasicAWSCredentials;
import com.amazonaws.auth.AWSStaticCredentialsProvider;
import com.amazonaws.client.builder.AwsClientBuilder;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3ClientBuilder;

public class TestJob {
    public static void uploadFile(String object_key, String from_bucket, String to_bucket) {
        AWSCredentials credentials = new BasicAWSCredentials("foo", "foo");
        String region = System.getenv().get("AWS_REGION");
        String lsHost = System.getenv().get("LOCALSTACK_HOSTNAME");
        String edgePort = System.getenv().get("EDGE_PORT");
        String s3URL = String.format("http://%s:%s", lsHost, edgePort);
        AmazonS3ClientBuilder builder = AmazonS3ClientBuilder.standard().
            withEndpointConfiguration(
                new AwsClientBuilder.EndpointConfiguration(s3URL, region)).
            withCredentials(new AWSStaticCredentialsProvider(credentials));
        builder.setPathStyleAccessEnabled(true);
        final AmazonS3 s3 = builder.build();
        try {
            s3.copyObject(from_bucket, object_key, to_bucket, object_key);
        } catch (AmazonServiceException e) {
            throw new RuntimeException(e);
        }
    }

    public static void main(String[] args) {
        final String USAGE = "\n" + "To run this example, supply the name (key) of an S3 object, the bucket name\n"
                + "that it's contained within, and the bucket to copy it to.\n" + "\n"
                + "Ex: CopyObject <objectname> <frombucket> <tobucket>\n";

        if (args.length < 3) {
            System.out.println(USAGE);
            System.exit(1);
        }

        String object_key = args[0];
        String from_bucket = args[1];
        String to_bucket = args[2];

        System.out.format("Copying object %s from bucket %s to %s\n", object_key, from_bucket, to_bucket);
        uploadFile(object_key, from_bucket, to_bucket);

        System.out.println("Done!");
    }
}
