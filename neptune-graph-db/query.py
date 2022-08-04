import os
import time
import boto3
from gremlin_python.driver import client as gremlin_client
from gremlin_python.structure.graph import Graph
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection

NEPTUNE_ENDPOINT = os.environ.get('NEPTUNE_ENDPOINT') or 'http://localhost:4566'
CLUSTER_ID = 'cluster123'


def poll_condition(condition, timeout: float = None, interval: float = 0.5) -> bool:
    remaining = 0
    if timeout is not None:
        remaining = timeout

    while not condition():
        if timeout is not None:
            remaining -= interval

            if remaining <= 0:
                return False

        time.sleep(interval)

    return True


def run_queries(cluster):
    cluster_url = 'ws://localhost:%s/gremlin' % cluster['Port']

    # test Client API
    print('Connecting to Neptune Graph DB cluster URL: %s' % cluster_url)
    graph_client = gremlin_client.Client(cluster_url, 'g')

    values = '[1,2,3,4]'
    print('Submitting values: %s' % values)
    result_set = graph_client.submit(values)
    future_results = result_set.all()
    results = future_results.result()
    print('Received values from cluster: %s' % results)
    assert results == [1, 2, 3, 4]

    future_result_set = graph_client.submitAsync('[1,2,3,4]')
    result_set = future_result_set.result()
    result = result_set.one()
    assert result == [1, 2, 3, 4]
    poll_condition(lambda: result_set.done.done(), timeout=3)
    assert result_set.done.done()
    graph_client.close()

    # test DriverRemoteConnection API
    graph = Graph()
    conn = DriverRemoteConnection(cluster_url, 'g')
    g = graph.traversal().withRemote(conn)
    vertices_before = g.V().toList()
    print('Existing vertices in the graph: %s' % vertices_before)
    print('Adding new vertices "v1" and "v2" to the graph')
    g.addV().property('id', 'v1').property('name', 'Vertex 1').next()
    g.addV().property('id', 'v2').property('name', 'Vertex 2').next()
    vertices_after = g.V().toList()
    print('New list of vertices in the graph: %s' % vertices_after)
    result = set(vertices_after) - set(vertices_before)
    assert len(result) == 2
    conn.close()


def create_graph_db():
    print('Creating Neptune Graph DB cluster "%s" - this may take a few moments ...' % CLUSTER_ID)
    client = connect_neptune()
    cluster = client.create_db_cluster(DBClusterIdentifier=CLUSTER_ID, Engine='neptune')['DBCluster']

    def is_cluster_available():
        clusters = client.describe_db_clusters()
        return clusters["DBClusters"][0]["Status"] == "available"

    cluster_available = poll_condition(is_cluster_available, timeout=15, interval=1)
    if not cluster_available:
        raise Exception("The server took too much time to start")

    return cluster


def delete_db(cluster=None):
    if cluster:
        cluster_id = cluster['DBClusterIdentifier']
    else:
        cluster_id = CLUSTER_ID
    print('Deleting Neptune Graph DB cluster "%s"' % cluster_id)
    client = connect_neptune()
    client.delete_db_cluster(DBClusterIdentifier=cluster_id)


def connect_neptune():
    return boto3.client('neptune', endpoint_url=NEPTUNE_ENDPOINT)


def main():
    instance = None
    try:
        instance = create_graph_db()
        run_queries(instance)
    finally:
        delete_db(instance)
    print('Done.')


if __name__ == '__main__':
    main()
