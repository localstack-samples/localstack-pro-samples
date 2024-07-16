local="${1:-local}"
tfoutput=$(terraform output -json)

application_id=$(echo $tfoutput | jq .application_id.value | tr -d '"')
role_arn=$(echo $tfoutput | jq .role_arn.value | tr -d '"')
bucket=$(echo $tfoutput | jq .s3_bucket.value | tr -d '"')

s3_bucket="s3://${bucket}"
s3a_bucket="s3a://${bucket}"

if [ $local = "local" ]; then
    # LocalStack doesn't yet support adding spark.archives, adding the environment from the volume added to localstack container
    env_path="/tmp/environment"
    AWS=awslocal
fi
if [ $local = "aws" ]; then
    env_path="environment"
    AWS=aws
    extra_conf="--conf spark.archives='${s3a_bucket}'/pyspark_deps.tar.gz#environment "
fi

$AWS s3 cp entrypoint.py ${s3_bucket}/entrypoint.py
$AWS s3 cp pyspark_deps.tar.gz ${s3_bucket}/pyspark_deps.tar.gz

job_run_result=$($AWS emr-serverless start-job-run \
    --application-id $application_id \
    --execution-role-arn $role_arn \
    --job-driver '{
        "sparkSubmit": {
            "entryPoint": "'${s3a_bucket}'/entrypoint.py",
            "sparkSubmitParameters": "'${extra_conf}' --conf spark.emr-serverless.driverEnv.PYSPARK_DRIVER_PYTHON='${env_path}'/bin/python --conf spark.emr-serverless.driverEnv.PYSPARK_PYTHON='${env_path}'/bin/python"
        }
    }' \
    --configuration-overrides '{
        "monitoringConfiguration": {
            "s3MonitoringConfiguration": {
                "logUri": "'${s3_bucket}'/logs/"
            }
        }
    }' | jq
)

echo $job_run_result
job_id=$(echo $job_run_result | jq .jobRunId | tr -d '"' )

while true; do
    job_run=$($AWS emr-serverless get-job-run --job-run-id $job_id --application-id $application_id)
    state=$(echo $job_run | jq .jobRun.state | tr -d '"' )
    echo "Job '${job_id}', State '${state}'. First run might take a few minutes."
    if [ "$state" = "SUCCESS" ]; then
        exit
    fi
    if [ "$state" = "FAILED" ]; then
        exit 1
    fi
    if [ "$local" = "aws" ]; then
        sleep 10
    fi
    sleep 1
done
