usage:           ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:         ## Install dependencies for all projects
	CMD='make install' make forEachDir

lint:            ## Run code linter for all projects
	CMD='make lint' make forEachDir

forEachDir:
	for d in $$(ls -d */); do (cd $$d; $(CMD)); done

.PHONY: usage install lint
