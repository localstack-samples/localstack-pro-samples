.PHONY: install run test-ci

# Install requirements
install:    
	docker pull ubuntu:focal
	docker tag ubuntu:focal localstack-ec2/ubuntu-focal-docker-ami:ami-00a001

# Run demo
run:
	./run.sh


start:
	localstack start -d

stop:
	localstack stop

ready:
	@localstack wait -t 30; echo "Localstack is ready to use!"

test-ci:
	make start install ready run stop
