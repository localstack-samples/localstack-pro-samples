usage:         ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:       ## Install dependencies for all projects
	MAKE_TARGET='install'; CMD='make $MAKE_TARGET || echo "No install target found in $PWD, skipping"' make for-each-dir

lint:          ## Run code linter for all projects
	CMD='make lint' make for-each-dir

start:         ## Start LocalStack infrastructure
	nohup localstack start &

stop:          ## Stop LocalStack infrastructure
	nohup localstack stop

for-each-dir:
	for d in $$(ls -d */); do echo "Making $$MAKE_TARGET in $$d"; ((cd $$d; $(CMD)) || echo "$$MAKE_TARGET in $$d FAILED"); done

show-logs:
	MAKE_TARGET='logs'; CMD='cat ./log.txt' make for-each-dir

test-ci-all:
	MAKE_TARGET='test-ci'; CMD='(test ! -e Makefile && echo SKIPPING TESTS IN $$d because there is no Makefile) || make test-ci' make for-each-dir

.PHONY: usage install lint start
