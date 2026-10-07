#!/usr/bin/env python3
"""
Configure Frontend Environment
Reads serverless-config.json and creates frontend .env.local file
"""
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_FILE = PROJECT_ROOT / 'serverless-config.json'
ENV_FILE = PROJECT_ROOT / 'frontend' / '.env.local'

def main():
    """Configure frontend environment"""
    print("🔧 Configuring Frontend Environment...")
    
    if not CONFIG_FILE.exists():
        print(f"❌ Configuration file not found: {CONFIG_FILE}")
        print("   Run 'python scripts/deploy-serverless.py' first")
        exit(1)
    
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
    
    env_content = f"""# EKart Store Frontend - Auto-generated Environment Configuration
# Generated from serverless-config.json

# API Gateway URL
NEXT_PUBLIC_API_URL={config['api_url']}

# AWS Cognito Configuration
NEXT_PUBLIC_AWS_REGION={config['region']}
NEXT_PUBLIC_USER_POOL_ID={config['user_pool_id']}
NEXT_PUBLIC_CLIENT_ID={config['client_id']}

# LocalStack Endpoint
NEXT_PUBLIC_AWS_ENDPOINT={config['endpoint']}

# Environment
NEXT_PUBLIC_ENV=development
"""
    
    with open(ENV_FILE, 'w') as f:
        f.write(env_content)
    
    print(f"✅ Frontend environment configured successfully!")
    print(f"   File: {ENV_FILE}")
    print()
    print("📋 Configuration:")
    print(f"   API URL: {config['api_url']}")
    print(f"   User Pool ID: {config['user_pool_id']}")
    print(f"   Client ID: {config['client_id']}")
    print()
    print("🎯 Next Steps:")
    print("   1. cd frontend")
    print("   2. npm run dev")
    print("   3. Open http://localhost:3000")
    print()

if __name__ == "__main__":
    main()
