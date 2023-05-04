import org.junit.Rule;
import org.junit.Test;
import org.testcontainers.containers.localstack.LocalStackContainer;
import org.testcontainers.utility.DockerImageName;
import software.amazon.awssdk.auth.credentials.AwsBasicCredentials;
import software.amazon.awssdk.auth.credentials.StaticCredentialsProvider;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.rds.RdsClient;
import software.amazon.awssdk.services.rds.model.CreateDbInstanceRequest;
import software.amazon.awssdk.services.rds.model.CreateDbInstanceResponse;
import software.amazon.awssdk.services.rds.model.DescribeDbInstancesRequest;
import software.amazon.awssdk.services.rds.model.DescribeDbInstancesResponse;

import java.net.InetAddress;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.UnknownHostException;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.fail;

public class TestRDS {

    private DockerImageName localstackImage = DockerImageName.parse("localstack/localstack-pro:latest");
    private String api_key = System.getenv("LOCALSTACK_API_KEY");

    /**
     * Start LocalStackContainer with exposed Ports. Those ports are used by services like RDS, where several databases can be started, running on different ports.
     * In this sample we only map 5 ports, however, depending on your use case you may need to map ports up to 4559
     */
    @Rule
    public LocalStackContainer localstack = new LocalStackContainer(localstackImage)
                                                        .withExposedPorts(4510, 4511, 4512, 4513, 4514) // TODO the port can have any value between 4510-4559, but LS starts from 4510
                                                        .withEnv("LOCALSTACK_API_KEY", api_key) // TODO add your API key here
                                                        .withServices(LocalStackContainer.EnabledService.named("rds"));


    @Test
    public void testRds() throws UnknownHostException, URISyntaxException {
        // create the rds client that will connect to the localstack testcontainer
        RdsClient rds = RdsClient
                .builder()
                .endpointOverride(localstack.getEndpointOverride(LocalStackContainer.EnabledService.named("rds")))
                .credentialsProvider(StaticCredentialsProvider.create(
                        AwsBasicCredentials.create(localstack.getAccessKey(), localstack.getSecretKey())
                )).region(Region.of(localstack.getRegion())).build();

        // create a db instance, by default it will use username "test" and password "test"
        CreateDbInstanceResponse response = rds.createDBInstance(CreateDbInstanceRequest.builder().dbName("hello").engine("postgres").build());
        String identifier = response.dbInstance().dbInstanceIdentifier();
        DescribeDbInstancesRequest request = DescribeDbInstancesRequest.builder().dbInstanceIdentifier(identifier).build();
        DescribeDbInstancesResponse describedb = rds.describeDBInstances(request);

        // wait for db to be ready
        while(! describedb.dbInstances().get(0).dbInstanceStatus().equalsIgnoreCase("available")) {
            describedb = rds.describeDBInstances(request);
        }

        // identify the port localstack provides for the instance
        int localstack_port = response.dbInstance().endpoint().port();

        // get the port it was mapped to, e.g. the one we can reach from host/the test
        int mapped_port = localstack.getMappedPort(localstack_port);
        try {
            // try to connect to database in our example we simply insert some dummy data
            String actual = RDS.test_connection(localstack.getHost(), mapped_port, "hello");
            String expected = "ID = 1\nNAME = world";
            assertEquals(actual, expected);
        } catch (Exception e) {
            fail("testing connection with database failed");
        }
        // rds database endpoint
        URI rds_database_uri = getMappedAddressForPort(localstack, localstack_port);
        System.out.println(rds_database_uri);

        // TODO do whatever with RDS instance using the uri/port

    }


    /**
     * Helper method to get the mapped address for any port. For services with varying ports.
     * Similar to {@link LocalStackContainer#getEndpointOverride} for fixed mapped services.
     *
     * @param localstack LocalStackContainer
     * @param localstack_port the port returned by LocalStack, e.g. for DescribeDBInstances
     * @return URI of the endpoint, reachable from host
     * @throws URISyntaxException
     * @throws UnknownHostException
     */
    public static URI getMappedAddressForPort(LocalStackContainer localstack, int localstack_port) throws URISyntaxException, UnknownHostException {
        String ipAddress = InetAddress.getByName(localstack.getHost()).getHostAddress();
        int mapped_port = localstack.getMappedPort(localstack_port);
        return new URI("http://" + ipAddress + ":" + mapped_port);

    }
}
