# LocalStack Demo: Chalice REST API

Simple demo application illustrating AWS Chalice integration in LocalStack. The AWS Chalice integration features a REST API which can be tested locally and put to production using the [LocalStack's AWS Chalice client](https://github.com/localstack/chalice-local).

## Prerequisites

- LocalStack
- Docker
- `chalice-local`

## Installing

To install the dependencies:

```sh
pip3 install -r requirements-dev.txt
```

## Running

Make sure that LocalStack is started:

```sh
localstack start -d
```

Start the local-server via:

```sh
chalice-local local
```

You will see the following logs on the terminal:

```sh
Serving on http://127.0.0.1:8000
```

## License

This code is available under the Apache 2.0 license.
