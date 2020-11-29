export AZURE = 1
export SERVICES = azure

usage:      ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

run:        ## Deploy and run the Azure test application
	@echo 'Creating Azure function archive'
	zip -r function.zip HttpTrigger requirements.txt host.json

	@echo 'Creating required resources'
	azlocal group create -g g1 -l l1
	azlocal appservice plan create -g g1 -n p1
	azlocal storage account create -g g1 -n sto1 --encryption-services blob \
		--encryption-services file --encryption-services queue --encryption-services table

	@echo 'Deploying Azure function'
	azlocal functionapp create  -g g1 -n func1 -s sto1 --os-type Linux --runtime python \
		--consumption-plan-location eastus
	azlocal functionapp deployment source config-zip --src function.zip -g g1 -n func1

	@echo 'Deploying Azure function via "func" CLI tools'
	# funclocal azure functionapp publish func1
	funclocal azure functionapp publish func1 --build local

test-ci:
	make install && make run || true

.PHONY: usage install run
