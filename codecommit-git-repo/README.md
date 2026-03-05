# CodeCommit Git Repository

| Key          | Value                               |
| ------------ | ----------------------------------- |
| Services     | CodeCommit                          |
| Integrations | AWS CLI, Git                        |
| Categories   | DevOps; Source Control              |

## Introduction

A demo application illustrating the use of the AWS CodeCommit API with LocalStack. The sample creates a Git repository via CodeCommit, commits and pushes files to it, and clones it in a fresh directory — all locally without connecting to AWS.

## Prerequisites

- A valid [LocalStack for AWS license](https://localstack.cloud/pricing). Your license provides a [`LOCALSTACK_AUTH_TOKEN`](https://docs.localstack.cloud/getting-started/auth-token/) to activate LocalStack. Set it with:
  ```bash
  export LOCALSTACK_AUTH_TOKEN=<your-auth-token>
  ```
  You can find your token on the [LocalStack Web Application](https://app.localstack.cloud/workspace/auth-token).
- [Docker](https://docs.docker.com/get-docker/)
- [`localstack` CLI](https://docs.localstack.cloud/getting-started/installation/#localstack-cli)
- [`awslocal` CLI](https://docs.localstack.cloud/user-guide/integrations/aws-cli/)
- [Git](https://git-scm.com/)

## Check prerequisites

```bash
make check
```

## Installation

```bash
make install
```

## Start LocalStack

```bash
make start
```

## Run the application

```bash
make run
```

The script:

- Creates a CodeCommit Git repository via the AWS API.
- Clones the repository to a temporary folder.
- Commits and pushes a test file to the repository.
- Clones the repository again to verify the committed file.

## License

This code is available under the Apache 2.0 license.
