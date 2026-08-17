# Testing RDS migrations locally with Prisma & LocalStack

In this sample application, we demonstrate how you can test your RDS migrations locally using Prisma and LocalStack. Prisma is a database ORM for Node.js applications, and this sample application showcases how you can use Prisma to run migration, generate model for the client, and run a small test inserting and querying data into the database.

## Prerequisites

* LocalStack
* Docker
* Node.js & `npm`
* `make`
* [`awslocal`](https://github.com/localstack/awscli-local)

## Start your LocalStack container

Start your LocalStack container with the `LOCALSTACK_AUTH_TOKEN` specified:

```bash
LOCALSTACK_AUTH_TOKEN=... DEBUG=1 localstack start
```

## Install the dependencies

Install the dependencies required for the application:

```bash
npm install
```

You can run the following command to see if Prisma is correctly installed:

```bash
npx prisma
```

## Create a local RDS database

You can now create a local RDS database using the `awslocal` CLI:

```bash
awslocal rds create-db-cluster \
    --db-cluster-identifier cluster1 \
    --engine=aurora-postgresql \
    --database-name test
```

**Note**: Check the port in the response, since you might have to adjust the `.env` file with the right port in the database URL.

## Run the migration

You can now run the migration using Prisma:

```bash
npx prisma migrate dev --name init
```

The following output should be displayed:

```bash
Environment variables loaded from .env
Prisma schema loaded from prisma/schema.prisma
Datasource "db": PostgreSQL database "test", schema "public" at "0.0.0.0:4510"

Applying migration `20240213041046_init`

The following migration(s) have been created and applied from new schema changes:

migrations/
  └─ 20240213041046_init/
    └─ migration.sql

Your database is now in sync with your schema.

✔ Generated Prisma Client (4.16.2 | library) to ./node_modules/@prisma/client in 63ms
```

## Generate models for the client

You can now generate the models for the client using Prisma:

```bash
npx generate
```

To run a small test inserting and querying data into the DB, you can run the following command:

```bash
npx ts-node main.ts
```

The following output should be displayed:

```bash
[
  {
    id: 1,
    email: 'alice@prisma.io',
    name: 'Alice',
    posts: [
      {
        id: 1,
        createdAt: 2024-02-13T04:13:39.901Z,
        updatedAt: 2024-02-13T04:13:39.901Z,
        title: 'Hello World',
        content: null,
        published: false,
        authorId: 1
      }
    ],
    profile: { id: 1, bio: 'I like turtles', userId: 1 }
  }
]
```

## Run a (re) migration

You can run another migration. A new schema is already created for you, and you just need to specify it while running the migration command.

```bash
npx prisma migrate dev --name init --schema=./prisma/schema-test.prisma
```

The following output should be displayed:

```bash
Environment variables loaded from .env
Prisma schema loaded from prisma/schema-test.prisma
Datasource "db": PostgreSQL database "test", schema "public" at "0.0.0.0:4510"

Applying migration `20240213041407_init`

The following migration(s) have been created and applied from new schema changes:

migrations/
  └─ 20240213041407_init/
    └─ migration.sql

Your database is now in sync with your schema.

✔ Generated Prisma Client (4.16.2 | library) to ./node_modules/@prisma/client in 62ms
```

## License

This code is licensed under the Apache 2.0 License. 
