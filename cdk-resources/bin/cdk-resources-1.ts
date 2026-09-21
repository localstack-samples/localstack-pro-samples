#!/usr/bin/env node
import * as cdk from '@aws-cdk/core';
import { CdkResources1Stack } from '../lib/cdk-resources-1-stack';

const app = new cdk.App();
const cdkResources1Stack = new CdkResources1Stack(app, 'CdkResources1Stack');
cdk.Tags.of(cdkResources1Stack).add('aws-apn-id', 'pc:9yq38ki5jw5mas7jhjthpgveo');
