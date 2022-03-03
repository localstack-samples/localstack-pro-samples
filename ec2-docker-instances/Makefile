.PHONY: install run test-ci

# Install requirements
install:    
	docker pull ubuntu:focal
	docker tag ubuntu:focal localstack-ec2/ubuntu-focal-docker-ami:ami-00a001

# Run demo
run: install
	./run.sh

# No op
test-ci:
	/bin/true
