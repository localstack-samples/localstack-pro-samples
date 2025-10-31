#!/usr/bin/env python3
"""
Cleanup Script - Remove all Lambda functions and API Gateway
Use before redeployment to avoid conflicts
"""
import boto3
import sys

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_PATH = PROJECT_ROOT / 'serverless-config.json'
with open(CONFIG_PATH, 'r') as _cfg_file:
    _CFG = json.load(_cfg_file)

ENDPOINT = _CFG.get('endpoint')
REGION = "us-east-1"
ENV = "dev"

def create_clients():
    config = {
        'endpoint_url': ENDPOINT,
        'region_name': REGION,
        'aws_access_key_id': 'test',
        'aws_secret_access_key': 'test'
    }
    return {
        'lambda': boto3.client('lambda', **config),
        'apigateway': boto3.client('apigateway', **config)
    }

def cleanup_lambda_functions(lambda_client):
    """Delete all ekart Lambda functions"""
    print("🗑️  Cleaning up Lambda functions...")
    
    try:
        response = lambda_client.list_functions()
        functions = response.get('Functions', [])
        
        deleted = 0
        for func in functions:
            func_name = func['FunctionName']
            if func_name.startswith('ekart-'):
                try:
                    lambda_client.delete_function(FunctionName=func_name)
                    print(f"  ✓ Deleted: {func_name}")
                    deleted += 1
                except Exception as e:
                    print(f"  ✗ Error deleting {func_name}: {e}")
        
        if deleted == 0:
            print("  ℹ️  No ekart functions found")
        else:
            print(f"  ✓ Deleted {deleted} Lambda functions")
        
    except Exception as e:
        print(f"  ✗ Error listing functions: {e}")

def cleanup_api_gateway(apigateway):
    """Delete all ekart API Gateways"""
    print("\n🗑️  Cleaning up API Gateway...")
    
    try:
        response = apigateway.get_rest_apis()
        apis = response.get('items', [])
        
        deleted = 0
        for api in apis:
            if api['name'].startswith('ekart-'):
                try:
                    apigateway.delete_rest_api(restApiId=api['id'])
                    print(f"  ✓ Deleted: {api['name']} ({api['id']})")
                    deleted += 1
                except Exception as e:
                    print(f"  ✗ Error deleting {api['name']}: {e}")
        
        if deleted == 0:
            print("  ℹ️  No ekart APIs found")
        else:
            print(f"  ✓ Deleted {deleted} API Gateways")
        
    except Exception as e:
        print(f"  ✗ Error listing APIs: {e}")

def main():
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║          🗑️  EKART STORE - CLEANUP SCRIPT                       ║
║                                                                  ║
║     Removes Lambda functions and API Gateway for fresh deploy   ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    # Check if LocalStack is running
    import requests
    try:
        response = requests.get(f'{ENDPOINT}/_localstack/health', timeout=5)
        if response.status_code != 200:
            print("❌ LocalStack is not running!")
            print("   Start LocalStack: docker-compose up localstack")
            sys.exit(1)
    except:
        print("❌ Cannot connect to LocalStack!")
        print("   Start LocalStack: docker-compose up localstack")
        sys.exit(1)
    
    print("✅ LocalStack is running\n")
    
    # Create clients
    clients = create_clients()
    
    # Cleanup
    cleanup_lambda_functions(clients['lambda'])
    cleanup_api_gateway(clients['apigateway'])
    
    print("\n" + "="*70)
    print("✅ CLEANUP COMPLETED")
    print("="*70)
    print("\n🎯 Next Steps:")
    print("  1. Run deployment: python scripts/deploy-serverless.py")
    print("  2. Or run quick deploy: python scripts/quick-deploy.py")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Cleanup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Cleanup error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
