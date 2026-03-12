# CodeCommit Git Repository

| Key          | Value                               |
| ------------ | ----------------------------------- |
| Services     | CodeCommit                          |
| Integrations | AWS CLI, Git                        |
| Categories   | DevOps; Source Control              |

## Introduction

A demo application illustrating the use of the AWS CodeCommit API with LocalStack. The sample creates a Git repository via CodeCommit, commits and pushes files to it, and clones it in a fresh directory — all locally without connecting to AWS.

## Prerequisites

- A valid [LocalStack for AWS license](https://localstack.cloud/pricing). Your license provides a [`LOCALSTACK_AUTH_TOKEN`](https://docs.localstack.cloud/getting-started/auth-token/) to activate LocalStack.
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
export LOCALSTACK_AUTH_TOKEN=<your-auth-token>
make start
```

## Run the application

```bash
make run
```

The script:

- Creates a CodeCommit Git repository via the CodeCommit API.
- Clones the repository to a temporary folder.
- Commits and pushes a test file to the repository.
- Clones the repository again to verify the committed file.

You should then see log messages similar to:

```
$ make run
-----
Step 1: Creating new CodeCommit git repository
-----
Step 2: Cloning repo to temporary folder
Cloning into '/tmp/test.codecommit.repo1'...
remote: counting objects: 21, done.
Receiving objects: 100% (21/21), 1.55 KiB | 1.55 MiB/s, done.
-----
Step 3: Committing and pushing new file to the repository
[master e7c599e] test_commit
 1 file changed, 1 insertion(+)
...
To git://localhost:4510/repo1
   7c1f7e8..e7c599e  master -> master
-----
Step 4: Cloning repo to second temporary folder
Cloning into '/tmp/test.codecommit.repo1.copy'...
-----
Step 5: Printing file content from second clone of repo
test file content 123
```

## License

This code is available under the Apache 2.0 license.
