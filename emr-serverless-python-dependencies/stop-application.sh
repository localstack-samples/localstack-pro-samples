local="${1:-local}"
tfoutput=$(terraform output -json)
application_id=$(echo $tfoutput | jq .application_id.value | tr -d '"')

if [ $local = "local" ]; then
    AWS=awslocal
fi
if [ $local = "aws" ]; then
    AWS=aws
fi

$AWS emr-serverless stop-application --application-id $application_id

while true; do
    state=$($AWS emr-serverless get-application --application-id $application_id | jq .application.state | tr -d '"')
    if [ "$state"  == "STOPPED" ]; then
        echo "Application Stopped"
        break
    fi
    echo "Waiting for application '${application_id}' to stop. Current state '${state}'"
    sleep 1
done