# Example using RDS with Localstack Testcontainers

Testcontainers need a special setup to use services like RDS, which may use any port to expose the database. The sample explains how the mapping works, and how you need to configure Testcontainers in order to connect to the RDS instance from your test.

## Prerequisites
- Docker running
- JDK 11+
- Maven 3.8+
- LocalStack Pro Auth Token in `LOCALSTACK_AUTH_TOKEN`

## Run Example
You can run the JUnit test either in your IDE or from the command line:

```
cd testcontainers-java-sample/LocalStackTestcontainers
export LOCALSTACK_AUTH_TOKEN=...  # required for RDS (Pro feature)
mvn -q -Dtest=TestRDS test
```

This will start a LocalStack Testcontainers instance, create a Postgres database via the RDS client, insert a row, and query it.


