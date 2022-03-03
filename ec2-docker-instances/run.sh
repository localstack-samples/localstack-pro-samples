#!/bin/bash

IFS=$'\n\t'
set -xeuo pipefail

# This is created in the install target of makefile
AMI_ID=ami-00a001

#
# Start an instance
#
printf '\e[31m%s\e[0m\n' "Starting an instance based on the Docker-backed AMI"
INSTANCE_ID=$(awslocal ec2 run-instances --image-id ${AMI_ID} --count 1 | jq --raw-output ".Instances[].InstanceId")

#
# Send command using AWS Systems Manager
#
printf '\e[31m%s\e[0m\n' "Sending an SSM command to this instance"
COMMAND_ID=$(awslocal ssm send-command --document-name "AWS-RunShellScript" \
                --document-version "1" \
                --instance-ids ${INSTANCE_ID} \
                --parameters "commands='cat lsb-release',workingDirectory=/etc" \
            | jq --raw-output .Command.CommandId)

# Pause for command to finish running
sleep 2

#
# Retrieve the results of the command
#
printf '\e[31m%s\e[0m\n' "Results of the SSM command"
awslocal ssm get-command-invocation --command-id ${COMMAND_ID} --instance-id ${INSTANCE_ID}

#
# Create a new AMI based off this running instance
#
printf '\e[31m%s\e[0m\n' "Taking a snapshot of the running instance into a new AMI"
awslocal ec2 create-image --instance-id ${INSTANCE_ID} --name localstack-sample-${RANDOM}

#
# Terminate the instance
#
printf '\e[31m%s\e[0m\n' "Terminating the instance"
awslocal ec2 terminate-instances --instance-ids ${INSTANCE_ID}
