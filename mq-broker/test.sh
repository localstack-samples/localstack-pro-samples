#!/bin/bash

echo "Creating MQ broker in LocalStack ..."
UUID=$(echo $RANDOM | md5sum | head -c 20)
broker_name="broker_${UUID}"
broker_id=$(awslocal mq create-broker --broker-name $broker_name --deployment-mode SINGLE_INSTANCE --engine-type ACTIVEMQ --engine-version='5.16.5' --host-instance-type 'mq.t2.micro' --auto-minor-version-upgrade --publicly-accessible --users='{"ConsoleAccess": true, "Groups": ["testgroup"],"Password": "QXwV*$iUM9USHnVv&!^7s3c@", "Username": "admin"}' | jq -r '.BrokerId')
echo "Created MQ broker with id: ${broker_id}"

# let broker fully start up
sleep 1
echo "Describe broker to get the endpoint"
broker_endpoint=$(awslocal mq describe-broker --broker-id $broker_id | jq -r '.BrokerInstances[0].ConsoleURL')
echo "Broker endpoint on ${broker_endpoint}"

echo "Sending message to broker"
curl -XPOST -d "body=message" http://admin:admin@${broker_endpoint:7}/api/message\?destination\=queue://orders.input

echo $"Cleaning up - deleting broker"
broker_id=$(awslocal mq delete-broker --broker-id $broker_id | jq -r '.BrokerId')
echo "Deleted Broker ${broker_id}"