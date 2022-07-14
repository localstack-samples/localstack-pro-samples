#!/bin/bash
set -e -x

REDSHIFT_CLUSTER_IDENTIFIER="redshiftcluster"
REDSHIFT_SCHEMA_NAME="public"
REDSHIFT_DATABASE_NAME="db1"
REDSHIFT_TABLE_NAME="sales"
REDSHIFT_USERNAME="crawlertestredshiftusername"
REDSHIFT_PASSWORD="crawlertestredshiftpassword"
GLUE_DATABASE_NAME="gluedb"
GLUE_CONNECTION_NAME="glueconnection"
GLUE_CRAWLER_NAME="gluecrawler"

# Tear-down function to cleanup on exit
function cleanup() {
  echo ""
  echo "(Cleanup) Deleting Redshift cluster."
  awslocal redshift delete-cluster --cluster-identifier $REDSHIFT_CLUSTER_IDENTIFIER 2> /dev/null || true
  echo "(Cleanup) Deleting Glue database."
  awslocal glue delete-database --name $GLUE_DATABASE_NAME 2> /dev/null || true
  echo "(Cleanup) Deleting Glue connection."
  awslocal glue delete-connection --connection-name $GLUE_CONNECTION_NAME 2> /dev/null || true
  echo "(Cleanup) Deleting Glue crawler."
  awslocal glue delete-crawler --name $GLUE_CRAWLER_NAME 2> /dev/null || true
}
trap cleanup EXIT

wait () {
  set -e -x
  command=$1
  field=$2
  expected=$3
  current=$($command | jq -r $field)
  while [ "$current" != "$expected" ]; do
    sleep 5
    echo "Waiting for state change. Current: $current / Expected: $expected"
    current=$($command | jq -r $field)
  done
}

# Cleanup
cleanup

# Create the redshift cluster
echo "Creating Redshift cluster..."
awslocal redshift create-cluster --cluster-identifier $REDSHIFT_CLUSTER_IDENTIFIER --db-name $REDSHIFT_DATABASE_NAME --master-username $REDSHIFT_USERNAME --master-user-password $REDSHIFT_PASSWORD --node-type n1
wait "awslocal redshift describe-clusters --cluster-identifier $REDSHIFT_CLUSTER_IDENTIFIER" ".Clusters[0].ClusterStatus" "available"
REDSHIFT_URL=$(awslocal redshift describe-clusters --cluster-identifier $REDSHIFT_CLUSTER_IDENTIFIER | jq -r '(.Clusters[0].Endpoint.Address) + ":" + (.Clusters[0].Endpoint.Port|tostring)')

# Create the Glue database, connection, and crawler
echo "Creating Glue db, connection, and crawler..."
awslocal glue create-database --database-input "{\"Name\": \"$GLUE_DATABASE_NAME\"}"
awslocal glue create-connection --connection-input "{\"Name\":\"$GLUE_CONNECTION_NAME\", \"ConnectionType\": \"JDBC\", \"ConnectionProperties\": {\"USERNAME\": \"$REDSHIFT_USERNAME\", \"PASSWORD\": \"$REDSHIFT_PASSWORD\", \"JDBC_CONNECTION_URL\": \"jdbc:redshift://$REDSHIFT_URL/$REDSHIFT_DATABASE_NAME\"}}"
awslocal glue create-crawler --name $GLUE_CRAWLER_NAME --database-name $GLUE_DATABASE_NAME --targets "{\"JdbcTargets\": [{\"ConnectionName\": \"$GLUE_CONNECTION_NAME\", \"Path\": \"$REDSHIFT_DATABASE_NAME/%/$REDSHIFT_TABLE_NAME\"}]}" --role r1

# Create a table in the redshift DB
echo "Creating table in Redshift DB..."
REDSHIFT_STATEMENT_ID=$(awslocal redshift-data execute-statement --cluster-identifier $REDSHIFT_CLUSTER_IDENTIFIER --database $REDSHIFT_DATABASE_NAME --sql \
  "create table $REDSHIFT_TABLE_NAME(salesid integer not null, listid integer not null, sellerid integer not null, buyerid integer not null, eventid integer not null, dateid smallint not null, qtysold smallint not null, pricepaid decimal(8,2), commission decimal(8,2), saletime timestamp)" | jq -r .Id)
wait "awslocal redshift-data describe-statement --id $REDSHIFT_STATEMENT_ID" ".Status" "FINISHED"

# Run the crawler
echo "Starting Crawler..."
awslocal glue start-crawler --name $GLUE_CRAWLER_NAME
wait "awslocal glue get-crawler --name $GLUE_CRAWLER_NAME" ".Crawler.State" "READY"

echo "Getting Glue table..."
awslocal glue get-table --database-name $GLUE_DATABASE_NAME --name "${REDSHIFT_DATABASE_NAME}_${REDSHIFT_SCHEMA_NAME}_${REDSHIFT_TABLE_NAME}"

echo "Done."