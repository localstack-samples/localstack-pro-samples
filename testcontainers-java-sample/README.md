# Example using RDS with Localstack Testcontainers

Testcontainers need a special setup to use services like RDS, which may use any port to expose the database.
The sample explains how the mapping works, and how you need to configure Testcontainers in order to connect to the RDS instance from your test.

## Run Example
* Import the project (e.g. in IntelliJ), 
* configure your LOCALSTACK_API_KEY as environment variable, 
* and then run  the test `TestRDS`.

It will create a LocalStack Testcontainer and a postgres database instance using RDSClient.
The database will then be filled with some data, and queried afterwards. 


