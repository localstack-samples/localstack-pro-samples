import os
import time

import boto3
import psycopg2

RDS_ENDPOINT = os.environ.get("RDS_ENDPOINT") or "http://localhost:4566"


def run_queries(instance):
    print("Run DB queries against RDS instance %s" % instance["DBInstanceIdentifier"])
    port = instance["Endpoint"]["Port"]
    host = instance["Endpoint"].get("Address") or "localhost.localstack.cloud"
    conn = None
    for _ in range(30):
        try:
            conn = psycopg2.connect(
                "dbname=test user=test password='test' host=%s port=%s" % (host, port)
            )
            break
        except psycopg2.OperationalError:
            time.sleep(2)
    if conn is None:
        raise RuntimeError("RDS Postgres endpoint did not become ready")

    with conn.cursor() as cur:
        cur.execute(
            'CREATE TABLE person ("id" INTEGER, "name" VARCHAR not null, PRIMARY KEY ("id"))'
        )
        cur.execute("INSERT INTO person VALUES (1, 'Jane')")
        cur.execute("INSERT INTO person VALUES (2, 'Alex')")
        cur.execute("INSERT INTO person VALUES (3, 'Maria')")
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM person")
        result = cur.fetchall()
        print(result)


def create_db():
    print("Creating RDS DB instance")
    client = connect_rds()
    instance = client.create_db_instance(
        Engine="postgres",
        DBInstanceClass="c1",
        DBInstanceIdentifier="i1",
        DBName="test",
        MasterUsername="test",
        MasterUserPassword="test",
    )
    return instance["DBInstance"]


def delete_db(instance):
    inst_id = instance["DBInstanceIdentifier"]
    print("Deleting RDS DB instance %s" % inst_id)
    client = connect_rds()
    client.delete_db_instance(DBInstanceIdentifier=inst_id, SkipFinalSnapshot=True)


def connect_rds():
    return boto3.client("rds", endpoint_url=RDS_ENDPOINT)


def main():
    instance = create_db()
    run_queries(instance)
    delete_db(instance)


if __name__ == "__main__":
    main()
