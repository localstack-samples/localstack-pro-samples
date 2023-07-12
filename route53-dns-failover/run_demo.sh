#!/usr/bin/env bash

# This is a demo script that showcases Route53 DNS failover in LocalStack
# Make sure the Docker Compose setup is running before executing this script

set -eux

HOSTED_ZONE_NAME=hello-localstack.com

# Create a hosted zone
HOSTED_ZONE_ID=$(awslocal route53 create-hosted-zone --name $HOSTED_ZONE_NAME --caller-reference foo | jq -r .HostedZone.Id)

# Create a health check that runs against the `http_echo` container
HEALTH_CHECK_ID=$(awslocal route53 create-health-check --caller-reference foobar --health-check-config '{
    "FullyQualifiedDomainName": "http_echo",
    "Port": 80,
    "ResourcePath": "/",
    "Type": "HTTP",
    "RequestInterval": 10
}' | jq -r .HealthCheck.Id)

# Create RRSets
awslocal route53 change-resource-record-sets --hosted-zone ${HOSTED_ZONE_ID#/hostedzone/} --change-batch '{
"Changes": [
    {
        "Action": "CREATE",
        "ResourceRecordSet": {
            "Name": "target1.'$HOSTED_ZONE_NAME'",
            "Type": "CNAME",
            "TTL": 60,
            "ResourceRecords": [{"Value": "target1.example.com"}]
        }
    },
    {
        "Action": "CREATE",
        "ResourceRecordSet": {
            "Name": "target2.'$HOSTED_ZONE_NAME'",
            "Type": "CNAME",
            "TTL": 60,
            "ResourceRecords": [{"Value": "target2.example.com"}]
        }
    }
]}'
awslocal route53 change-resource-record-sets --hosted-zone-id ${HOSTED_ZONE_ID#/hostedzone/} --change-batch '{
"Changes": [
    {
        "Action": "CREATE",
        "ResourceRecordSet": {
            "Name": "test.'$HOSTED_ZONE_NAME'",
            "Type": "CNAME",
            "SetIdentifier": "target1",
            "AliasTarget": {
                "HostedZoneId": "'${HOSTED_ZONE_ID#/hostedzone/}'",
                "DNSName": "target1.'$HOSTED_ZONE_NAME'",
                "EvaluateTargetHealth": true
            },
            "HealthCheckId": "'${HEALTH_CHECK_ID}'",
            "Failover": "PRIMARY"
        }
    },
    {
        "Action": "CREATE",
        "ResourceRecordSet": {
            "Name": "test.'$HOSTED_ZONE_NAME'",
            "Type": "CNAME",
            "SetIdentifier": "target2",
            "AliasTarget": {
                "HostedZoneId": "'${HOSTED_ZONE_ID#/hostedzone/}'",
                "DNSName": "target2.'$HOSTED_ZONE_NAME'",
                "EvaluateTargetHealth": true
            },
            "Failover": "SECONDARY"
        }
    }
]}'

# Get the IP address of the LocalStack container on the Docker bridge
LOCALSTACK_DNS_SERVER=$(docker inspect localstack_main | jq -r '.[0].NetworkSettings.Networks."route53-dns-failover_sweet_mahavira".IPAddress')
LOCALSTACK_DNS_SERVER=localhost

# This IP address is used to query the LocalStack DNS server
# This should return `target1.example.com` as the healthcheck is currently passing
dig @$LOCALSTACK_DNS_SERVER +noall +answer test.hello-localstack.com CNAME

# Make the healthcheck fail by pointing it to a nonexistent host
awslocal route53 update-health-check --health-check-id ${HEALTH_CHECK_ID} --fully-qualified-domain-name bad-host-p45e8eG94rK.com

# Wait for the healthcheck to refresh
sleep 12

# This should return the failover `target2.example.com`
dig @$LOCALSTACK_DNS_SERVER +noall +answer test.hello-localstack.com CNAME
