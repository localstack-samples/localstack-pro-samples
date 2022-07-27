usage:         ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:       ## Install dependencies for all projects
	CMD='make install || echo "No install target found in $PWD, skipping"' make for-each-dir

lint:          ## Run code linter for all projects
	CMD='make lint' make for-each-dir

start:         ## Start LocalStack infrastructure
	nohup localstack start &

stop:          ## Stop LocalStack infrastructure
	nohup localstack stop

for-each-dir:
	for d in $$(ls -d */); do echo "Running tests in $$d"; ((cd $$d; $(CMD)) || echo "test in $$d FAILED") && localstack stop; done

test-ci-all:
	CMD='test ! -e Makefile || make test-ci' make for-each-dir

.PHONY: usage install lint start
