usage:         ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:       ## Install dependencies for all projects
	MAKE_TARGET='install' make for-each-dir

lint:          ## Run code linter for all projects
	CMD='make lint' make for-each-dir

start:         ## Start LocalStack infrastructure
	nohup localstack start &

stop:          ## Stop LocalStack infrastructure
	nohup localstack stop

for-each-dir:
	./make-for-each.sh $$MAKE_TARGET $$CMD

test-ci-all:
	MAKE_TARGET='test-ci' make for-each-dir

.PHONY: usage install lint start
