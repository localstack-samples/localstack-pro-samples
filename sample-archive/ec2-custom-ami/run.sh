#!/bin/bash

IMAGE_URL=https://cdn.amazonlinux.com/os-images/2.0.20191217.0/virtualbox/amzn2-virtualbox-2.0.20191217.0-x86_64.xfs.gpt.vdi
BUCKET=test-bucket
IMAGE_FILE=amzn2.vdi

test -e $IMAGE_FILE || wget -O $IMAGE_FILE $IMAGE_URL

VPC_ID=$(awslocal ec2 create-vpc --cidr-block 0.0.0.0/24 | jq -r '.Vpc.VpcId')
SUB_ID=$(awslocal ec2 create-subnet --cidr-block 0.0.0.0/26 --vpc-id $VPC_ID | jq -r '.Subnet.SubnetId')

perl -i -pe 's|"S3Key": .*|"S3Key": "'$PWD'/amzn2.vdi"|' containers.json
IMAGE_ID=$(awslocal ec2 import-image --description "Test VM image" --license-type BYOL --disk-containers file://containers.json | jq -r '.ImageId')

perl -i -pe 's/"source_ami": .*/"source_ami": "'$IMAGE_ID'",/' packer.json
perl -i -pe 's/"subnet_id": .*/"subnet_id": "'$SUB_ID'",/' packer.json
perl -i -pe 's|"ssh_private_key_file": .*|"ssh_private_key_file": "'$PWD'/localstack.id_rsa",|' packer.json

echo "Starting image creation using packer"
packer build packer.json || sudo packer build packer.json
