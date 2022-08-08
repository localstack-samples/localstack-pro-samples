#!/usr/bin/env bash

# Tear-down function to cleanup on exit
function finish {
  echo ""
  # Delete the cluster (if available)
  echo "(Cleanup) Deleting Kafka cluster."
  awslocal kafka delete-cluster --cluster-arn  $cluster_arn 2> /dev/null || true
  # Delete the schema registry
  echo "(Cleanup) Deleting registry."
  awslocal glue delete-registry --registry-id RegistryName=unicorn-ride-request-registry 2> /dev/null || true
}
trap finish EXIT

# Function to wait for a key input before continuing (only in interactive mode)
if [ "$1" = "-it" ]; then
  function step {
    if [ -n "$1" ]; then
      echo ""
      echo "$1"
    fi
    read -n 1 -p "Continue by pressing any key." -r
    echo ""
  }
else
  function step {
    if [ -n "$1" ]; then
      echo ""
      echo "$1"
      echo ""
    fi
  }
fi

step "Start with creating a Kafka cluster..."
cluster_arn=$(set -x;awslocal kafka create-cluster \
  --cluster-name "unicorn-ride-cluster" \
  --kafka-version "2.2.1" \
  --number-of-broker-nodes 1 \
  --broker-node-group-info "{\"ClientSubnets\": [], \"InstanceType\":\"kafka.m5.xlarge\"}" | jq -r .ClusterArn)

state=$(set -x; awslocal kafka describe-cluster --cluster-arn $cluster_arn | jq -r .ClusterInfo.State)

for i in {1..35}; do
  echo "Waiting for Kafka cluster to become ACTIVE (current status: $state)..."
  sleep 4
  if [ "$state" == ACTIVE ]; then
    break
  elif [ "$state" == FAILED ]; then
    echo "Cluster creation FAILED, exiting..."
    exit 1
  fi
  state=$(awslocal kafka describe-cluster --cluster-arn $cluster_arn | jq -r .ClusterInfo.State)
done

if [ "$state" != ACTIVE  ]; then
  echo "Gave up waiting on Cluster, exiting..."
  exit 1
fi
bootstrap_broker=$(set -x; awslocal kafka get-bootstrap-brokers --cluster-arn  $cluster_arn | jq -r .BootstrapBrokerString)
echo "Kafka Bootstrap Broker: $bootstrap_broker"

step "The Kafka cluster is ready. Let's create a Glue Schema Registry..."
(set -x; awslocal glue create-registry --registry-name unicorn-ride-request-registry)

step "Create the AVRO schema in the new registry (with compatibility BACKWARD)..."
schema_arn=$(set -x; awslocal glue create-schema \
  --registry-id RegistryName="unicorn-ride-request-registry" \
  --schema-name unicorn-ride-request-schema-avro \
  --compatibility BACKWARD \
  --data-format AVRO \
  --schema-definition "file://producer/src/main/resources/avro/unicorn_ride_request_v1.avsc" | jq -r .SchemaArn)

step "Check if the schema has been created successfully..."
(set -x; awslocal glue get-schema \
  --schema-id SchemaArn=$schema_arn)

step "Check if the schema version has been created correctly..."
(set -x; awslocal glue get-schema-version \
  --schema-id SchemaArn=$schema_arn \
  --schema-version-number LatestVersion=True)

step "Prepare the Java clients (clean modules, generate AVRO model classes, compile the modules)..."
(set -x; mvn clean install)

step "Run the producer (which sends 100 records compliant to version 1 of the schema)..."
(set -x; mvn -pl producer exec:java -Dexec.args="--bootstrap-servers $bootstrap_broker")

step "Run the consumer (which receives 100 records - expecting the records to be compliant to version 1 of the schema)..."
(set -x; mvn -pl consumer exec:java -Dexec.args="--bootstrap-servers $bootstrap_broker")

step "Run a new producer (automatically registers a new schema which removes a required field - i.e. BACKWARD compatible to v1)..."
(set -x; mvn -pl producer-2 exec:java -Dexec.args="--bootstrap-servers $bootstrap_broker")

step "Get a diff between the initial version and the version registered by the new producer..."
(set -x; awslocal glue get-schema-versions-diff \
  --schema-id SchemaArn=$schema_arn \
  --schema-diff-type SYNTAX_DIFF \
  --first-schema-version-number VersionNumber=1 \
  --second-schema-version-number LatestVersion=True | jq -r)

step "Expected failure: Execute a producer which tries to register an incompatible schema..."
(set -x; mvn -pl producer-3 exec:java -Dexec.args="--bootstrap-servers $bootstrap_broker")

step "Check that the newly registered schema is in state 'FAILED'..."
awslocal glue get-schema-version \
  --schema-id SchemaArn=$schema_arn \
  --schema-version-number VersionNumber=3

step "Expected failure: Execute an incompatible (outdated) consumer..."
(set -x; mvn -pl consumer exec:java -Dexec.args="--bootstrap-servers $bootstrap_broker")

step "Execute a compatible (updated) consumer..."
(set -x; mvn -pl consumer-2 exec:java -Dexec.args="--bootstrap-servers $bootstrap_broker")

