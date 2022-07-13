# LocalStack Demo: Manage Files in a CodeCommit Git Repository

Simple demo application illustrating the use of the AWS CodeCommit API in LocalStack.

## Prerequisites

* LocalStack
* Docker
* `make`

## Installing

To install the dependencies:
```
make install
```

## Running

Make sure that LocalStack is started:
```
LOCALSTACK_API_KEY=... DEBUG=1 localstack start
```

The following command runs the test application locally, creates an Git repository via the AWS CodeCommit API locally, commits and pushes a test file to the repository, and then checks out the file in a fresh clone of the repository:
```
make run
```

You should then see a couple of log messages in the terminal:
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
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Delta compression using up to 8 threads
Compressing objects: 100% (2/2), done.
Writing objects: 100% (3/3), 292 bytes | 292.00 KiB/s, done.
Total 3 (delta 1), reused 0 (delta 0)
To git://localhost:4510/repo1
   7c1f7e8..e7c599e  master -> master
-----
Step 4: Cloning repo to second temporary folder
Cloning into '/tmp/test.codecommit.repo1.copy'...
remote: counting objects: 24, done.
Receiving objects: 100% (24/24), 1.78 KiB | 608.00 KiB/s, done.
-----
Step 5: Printing file content from second clone of repo
test file content 123
```

## License

This code is available under the Apache 2.0 license.
