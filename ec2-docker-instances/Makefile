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
	@echo
	localstack stop
ready:
	@echo Waiting on the LocalStack container...
	@localstack wait -t 30 && echo Localstack is ready to use! || (echo Gave up waiting on LocalStack, exiting. && exit 1)

logs:
	@localstack logs > logs.txt

test-ci:
	make start install ready run; make logs; make stop
