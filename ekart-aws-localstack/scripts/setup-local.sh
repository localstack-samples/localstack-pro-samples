#!/bin/bash
set -e
echo "🚀 Setting up EKart Store locally..."
# Check prerequisites
command -v docker >/dev/null 2>&1 || { echo "Docker is required but not installed. Aborting." >&2; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo "Docker Compose is required but not installed. Aborting." >&2; exit 1; }
command -v node >/dev/null 2>&1 || { echo "Node.js is required but not installed. Aborting." >&2; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "Python 3 is required but not installed. Aborting." >&2; exit 1; }
# Create necessary directories
mkdir -p tmp/localstack
mkdir -p logs
mkdir -p backup
# Copy environment files
cp .env.example .env
cd frontend && cp .env.local.example .env.local && cd ..
echo "📦 Installing dependencies..."
make install
echo "🐳 Starting LocalStack..."
docker-compose up -d localstack
echo "⏳ Waiting for LocalStack to be ready..."
./scripts/wait-for-localstack.sh
echo "🏗️ Deploying infrastructure..."
make deploy-infra
echo "🌱 Seeding initial data..."
make seed-data
echo "🎉 Setup completed!"
echo ""
echo "Next steps:"
echo "1. Run 'make start' to start all services"
echo "2. Visit http://localhost:3000 for the frontend"
echo "3. Visit http://localhost:8000/api/docs for API documentation"
echo "4. Visit http://localhost:4566/_localstack/cockpit for LocalStack dashboard"
