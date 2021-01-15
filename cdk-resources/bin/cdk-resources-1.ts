#!/usr/bin/env node
import * as cdk from '@aws-cdk/core';
import { CdkResources1Stack } from '../lib/cdk-resources-1-stack';

const app = new cdk.App();
new CdkResources1Stack(app, 'CdkResources1Stack');
