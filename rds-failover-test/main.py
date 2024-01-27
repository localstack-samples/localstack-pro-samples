import boto3
import time

ENDPOINT_URL = "http://localhost:4566"

global_cluster_id = "global-cluster-1"
primary_cluster_id = "rds-cluster-1"
secondary_cluster_id = "rds-cluster-2"
secondary_cluster2_id = f"rds-cluster-3"
db_instance_id_1 = "rds-inst-1-1"
db_instance_id_2 = "rds-inst-1-2"
region_1 = "us-east-1"
region_2 = "us-west-1"
region_3 = "us-west-2"


class State:
    primary_cluster_arn = None
    secondary_cluster_arn = None
    secondary_cluster_arn_2 = None


def client(service, **kwargs):
    kwargs.setdefault("region_name", region_1)
    kwargs.setdefault("aws_access_key_id", "test")
    kwargs.setdefault("aws_secret_access_key", "test")
    return boto3.client(service, endpoint_url=ENDPOINT_URL, **kwargs)


def poll_condition(condition, timeout: float = None, interval: float = 0.5) -> bool:
    remaining = timeout or 0
    while not condition():
        if timeout is not None:
            remaining -= interval
            if remaining <= 0:
                return False
        time.sleep(interval)
    return True


def create_cluster_with_instances():
    """Create a global cluster with two clusters + instances"""

    db_type = "aurora-postgresql"
    engine_version = "13.7"
    print(f"Creating global cluster '{global_cluster_id}'")
    rds_client = client("rds")
    rds_client.create_global_cluster(
        GlobalClusterIdentifier=global_cluster_id,
        Engine=db_type,
        EngineVersion=engine_version,
    )

    # create primary
    instance_class = "db.r5.large"
    print(f"Creating primary DB cluster '{primary_cluster_id}'")
    result = rds_client.create_db_cluster(
        DBClusterIdentifier=primary_cluster_id,
        Engine=db_type,
        DatabaseName="test",
        EngineVersion=engine_version,
        GlobalClusterIdentifier=global_cluster_id,
    )
    State.primary_cluster_arn = result["DBCluster"]["DBClusterArn"]

    # add instance to the primary cluster
    rds_client.create_db_instance(
        DBClusterIdentifier=primary_cluster_id,
        DBInstanceIdentifier=db_instance_id_1,
        Engine=db_type,
        EngineVersion=engine_version,
        DBInstanceClass=instance_class,
    )
    # add a second instance to the primary cluster
    rds_client.create_db_instance(
        DBClusterIdentifier=primary_cluster_id,
        DBInstanceIdentifier=db_instance_id_2,
        Engine=db_type,
        EngineVersion=engine_version,
        DBInstanceClass=instance_class,
    )

    # add a secondary cluster
    print(f"Creating secondary DB cluster '{secondary_cluster_id}'")
    rds_client_2 = client("rds", region_name=region_2)
    result = rds_client_2.create_db_cluster(
        DBClusterIdentifier=secondary_cluster_id,
        Engine=db_type,
        EngineVersion=engine_version,
        GlobalClusterIdentifier=global_cluster_id,
    )
    State.cluster_arn_secondary = result["DBCluster"]["DBClusterArn"]

    # add instance to the secondary cluster
    rds_client_2.create_db_instance(
        DBClusterIdentifier=secondary_cluster_id,
        DBInstanceIdentifier=db_instance_id_1,
        Engine=db_type,
        EngineVersion=engine_version,
        DBInstanceClass=instance_class,
    )

    # describe cluster
    rds_client_2.describe_db_clusters(DBClusterIdentifier=secondary_cluster_id)

    # add another secondary cluster (headless - no instances)
    rds_client_3 = client("rds", region_name=region_3)
    result = rds_client_3.create_db_cluster(
        DBClusterIdentifier=secondary_cluster2_id,
        Engine=db_type,
        EngineVersion=engine_version,
        GlobalClusterIdentifier=global_cluster_id,
    )
    State.cluster_arn_secondary_2 = result["DBCluster"]["DBClusterArn"]


def check_global_clusters_writer_flag():
    """List the global cluster members and assert that `IsWriter` is set for the primary cluster"""

    rds_client_3 = client("rds", region_name=region_3)
    result = rds_client_3.describe_global_clusters(
        GlobalClusterIdentifier=global_cluster_id
    )
    members = result["GlobalClusters"][0]["GlobalClusterMembers"]
    assert len(members) == 3
    members_map = {m["DBClusterArn"]: m for m in members}
    assert members_map.get(State.primary_cluster_arn)["IsWriter"]
    assert not members_map.get(State.cluster_arn_secondary)["IsWriter"]
    assert not members_map.get(State.cluster_arn_secondary_2)["IsWriter"]

    assert (
        State.cluster_arn_secondary
        in members_map.get(State.primary_cluster_arn)["Readers"]
    )
    assert (
        State.cluster_arn_secondary_2
        in members_map.get(State.primary_cluster_arn)["Readers"]
    )

    assert not result["GlobalClusters"][0].get("FailoverState")


def check_db_clusters_writer_flag():
    """
    Run the describe-db-clusters for primary + secondary clusters and show that only the first instance in
    the primary cluster has the flag `IsClusterWriter` set to True, all other instances should return False
    """

    print("Running assertions, to ensure the cluster writer has been updated")

    #   primary:
    rds_client = client("rds")
    describe = rds_client.describe_db_clusters(DBClusterIdentifier=primary_cluster_id)
    members_map = {
        p["DBInstanceIdentifier"]: p
        for p in describe["DBClusters"][0]["DBClusterMembers"]
    }
    # assert that first instance in primary cluster is the writer
    assert len(members_map) == 2
    assert members_map.get(db_instance_id_1)["IsClusterWriter"]
    assert not members_map.get(db_instance_id_2)["IsClusterWriter"]

    #   secondary #1:
    rds_client_2 = client("rds", region_name=region_2)
    describe = rds_client_2.describe_db_clusters(
        DBClusterIdentifier=secondary_cluster_id
    )
    members_map = {
        p["DBInstanceIdentifier"]: p
        for p in describe["DBClusters"][0]["DBClusterMembers"]
    }

    assert len(members_map) == 1
    assert not members_map.get(db_instance_id_1)["IsClusterWriter"]


def run_global_cluster_failover():
    """Run the failover via failover-global-cluster to switch primary with one secondary cluster"""

    print("Start global DB cluster failover ...")
    rds_client = client("rds")
    rds_client.failover_global_cluster(
        GlobalClusterIdentifier=global_cluster_id,
        TargetDbClusterIdentifier=State.cluster_arn_secondary,
    )

    def check_failover_started():
        res = rds_client.describe_global_clusters(
            GlobalClusterIdentifier=global_cluster_id
        )
        status = res["GlobalClusters"][0].get("FailoverState", {}).get("Status")
        return status in ("failing-over", "switching-over")

    # assert that status is `failing-over`
    assert poll_condition(check_failover_started, timeout=40, interval=1)

    def check_failover_finished():
        res = rds_client.describe_global_clusters(
            GlobalClusterIdentifier=global_cluster_id
        )
        return not res["GlobalClusters"][0].get("FailoverState")

    # wait for failover to complete
    assert poll_condition(check_failover_finished, timeout=40, interval=1)


def assert_global_cluster_writer_switched():
    """Assert that the describe-global-clusters + describe-db-clusters correctly show that the writer switched"""

    # assert that instances in primary cluster are no longer the writer
    rds_client = client("rds")
    describe = rds_client.describe_db_clusters(DBClusterIdentifier=primary_cluster_id)
    members_map = {
        p["DBInstanceIdentifier"]: p
        for p in describe["DBClusters"][0]["DBClusterMembers"]
    }
    assert len(members_map) == 2
    assert not members_map.get(db_instance_id_1)["IsClusterWriter"]
    assert not members_map.get(db_instance_id_2)["IsClusterWriter"]

    # assert that first instance in secondary cluster is now the writer
    rds_client_2 = client("rds", region_name=region_2)
    describe = rds_client_2.describe_db_clusters(
        DBClusterIdentifier=secondary_cluster_id
    )
    members_map = {
        p["DBInstanceIdentifier"]: p
        for p in describe["DBClusters"][0]["DBClusterMembers"]
    }
    assert len(members_map) == 1
    assert members_map.get(db_instance_id_1)["IsClusterWriter"]

    # remove secondary #2 cluster (headless) from global cluster:
    rds_client_3 = client("rds", region_name=region_3)
    describe = rds_client_3.describe_db_clusters(
        DBClusterIdentifier=secondary_cluster2_id
    )
    assert not describe["DBClusters"][0]["DBClusterMembers"]
    rds_client.remove_from_global_cluster(
        GlobalClusterIdentifier=global_cluster_id,
        DbClusterIdentifier=State.cluster_arn_secondary_2,
    )

    def check_removed_global_cluster():
        res = rds_client.describe_global_clusters(
            GlobalClusterIdentifier=global_cluster_id
        )
        return len(res["GlobalClusters"][0].get("GlobalClusterMembers")) == 2

    # assert that we now have 2 global cluster members (instead of 3 previously)
    assert poll_condition(check_removed_global_cluster, timeout=30, interval=0.5)


def main():
    # (1) create a global cluster with two clusters + instances
    create_cluster_with_instances()

    # (2) lists the members via describe-global-clusters and assert that `IsWriter` is set for the primary cluster
    check_global_clusters_writer_flag()

    # (3) run the describe-db-clusters for primary + secondary clusters and show that only the first instance in
    #   the primary cluster has the flag `IsClusterWriter` set to True, all other instances should return False
    check_db_clusters_writer_flag()

    # (4) run the failover via failover-global-cluster to switch primary with one secondary cluster
    run_global_cluster_failover()

    # (5) assert that the describe-global-clusters + describe-db-clusters correctly show that the writer switched
    assert_global_cluster_writer_switched()

    print("✅ Test done - all assertions succeeded")


if __name__ == "__main__":
    main()
