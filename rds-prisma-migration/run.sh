#!/bin/bash

npm install
npx prisma
awslocal rds create-db-cluster \
    --db-cluster-identifier cluster1 \
    --engine=aurora-postgresql \
    --database-name test \
    --output text
sleep 30
npx prisma migrate dev --name init
npx generate
npx ts-node main.ts
npx prisma migrate dev --name init --schema=./prisma/schema-test.prisma
