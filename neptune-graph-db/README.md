# LocalStack Demo: Neptune Graph Database

Simple demo application illustrating the use of Neptune Graph DB queries locally, using LocalStack.

## Prerequisites

* LocalStack (Pro version)
* Docker
* Python
* `make`
* [`awslocal`](https://github.com/localstack/awscli-local)

## Installing

To install the dependencies:
```
make install
```

## Starting LocalStack

Make sure that LocalStack is started:
```
LOCALSTACK_API_KEY=... DEBUG=1 localstack start
```

## Running

Run the scenario Python script `query.py` as follows:
```
make run
```

You should see some logs from the script, similar to the output below:
```
Creating Neptune Graph DB cluster "cluster123" - this may take a few moments ...
Connecting to Neptune Graph DB cluster URL: ws://localhost:4510/gremlin
Submitting values: [1,2,3,4]
Received values from cluster: [1, 2, 3, 4]
Existing vertices in the graph: []
Adding new vertices "v1" and "v2" to the graph
New list of vertices in the graph: [v[0], v[3]]
Deleting Neptune Graph DB cluster "cluster123"
```
_Note: when running the scenario consecutively, it may takes some time to free the port used by Neptune._
## License

The code in this sample repo is available under the Apache 2.0 license.
