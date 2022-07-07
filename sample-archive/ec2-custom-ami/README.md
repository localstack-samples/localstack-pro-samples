# IMPORTANT
The demostrated functionality has been removed from LocalStack

# LocalStack Demo: EC2 VMs and Custom Images using Packer

Simple demo application illustrating EC2 virtual machines (VMs) and building images locally, using LocalStack.

## Prerequisites

* LocalStack
* Docker
* `make`
* [`awslocal`](https://github.com/localstack/awscli-local)
* [`packer`](https://www.packer.io)
* `VirtualBox` on Mac OS

**Note:** This demo currently only works using VirtualBox on Mac OS. Support for additional operating systems and hypervisors will be added soon.

Note: This demo may require downloading a few large files (e.g., virtual machine base image) - please ensure that you're on a fast and stable internet connection.

## Installing

To install the dependencies:
```
make install
```

## App Details

Please refer to the `containers.json` and `packer.json` configuration files.

## Running

Make sure that LocalStack is started with the following `SERVICES` configuration:
```
LOCALSTACK_API_KEY=... DEBUG=1 SERVICES=cloudformation,ec2 localstack start
```

Run the application and trigger the virtual machine build process:
```
make run
```

You should see a temporary virtual machine getting started in VirtualBox, which then gets configured using the initialization script `setup.sh`. .

As the script is running, you should see some logs and a success output in the terminal:
```
...
Starting image creation using packer
amazon-ebs: output will be in this color.

==> amazon-ebs: Prevalidating any provided VPC information
==> amazon-ebs: Prevalidating AMI Name: amzn2_modified_ami
    amazon-ebs: Found Image ID: ami-9982a8ce
==> amazon-ebs: Using existing SSH private key
==> amazon-ebs: Creating temporary security group for this instance: packer_5e40764b-c37b-bb95-1e45-dc60bbab767d
==> amazon-ebs: Authorizing access to port 22 from [0.0.0.0/0] in the temporary security groups...
==> amazon-ebs: Launching a source AWS instance...
==> amazon-ebs: Adding tags to source instance
    amazon-ebs: Adding tag: "Name": "Packer Builder"
    amazon-ebs: Instance ID: i-14cb71067b38416b1
==> amazon-ebs: Waiting for instance (i-14cb71067b38416b1) to become ready...
==> amazon-ebs: Using ssh communicator to connect: 127.0.100.2
==> amazon-ebs: Waiting for SSH to become available...
==> amazon-ebs: Connected to SSH!
==> amazon-ebs: Provisioning with shell script: ./setup.sh
    amazon-ebs: Test - Installing dependencies inside EC2 virtual machine
==> amazon-ebs: Stopping the source instance...
    amazon-ebs: Stopping instance
==> amazon-ebs: Waiting for the instance to stop...
==> amazon-ebs: Creating AMI amzn2_modified_ami from instance i-14cb71067b38416b1
    amazon-ebs: AMI: ami-86c09caf
==> amazon-ebs: Waiting for AMI to become ready...
==> amazon-ebs: Terminating the source AWS instance...
==> amazon-ebs: Cleaning up any extra volumes...
==> amazon-ebs: No volumes to clean up, skipping
==> amazon-ebs: Deleting temporary security group...
Build 'amazon-ebs' finished.

==> Builds finished. The artifacts of successful builds are:
--> amazon-ebs: AMIs were created:
us-east-1: ami-86c09caf
```

The test SSH keys are included in this repository. To manually ssh into the instance, you can use this command (please note that the IP `127.0.100.2` is extracted from the output above):
```
$ ssh -i localstack.id_rsa ec2-user@127.0.100.2

__|  __|_  )
_|  (     /   Amazon Linux 2 AMI
___|\___|___|

https://aws.amazon.com/amazon-linux-2/

[ec2-user@localstack ~]$
```

## License

This code is available under the Apache 2.0 license.
