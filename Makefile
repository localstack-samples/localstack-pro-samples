usage:         ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:       ## Install dependencies for all projects
	MAKE_TARGET='install' make for-each-dir

lint:          ## Run code linter for all projects
	MAKE_TARGET='lint' make for-each-dir

start:         ## Start LocalStack infrastructure
	localstack start -d

ready:         ## Check if the LocalStack container is up and running.
	localstack wait -t 20 && echo "LocalStack is ready to use!"

stop:          ## Stop LocalStack infrastructure
	localstack stop

for-each-dir:
	./make-for-each.sh $$MAKE_TARGET $$CMD

test-ci-all:
	MAKE_TARGET='test-ci' make for-each-dir

.PHONY: usage install lint start ready stop for-each-dir test-ci-all
