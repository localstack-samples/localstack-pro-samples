.PHONY: help install start stop restart logs test clean build deploy

# Default environment
ENV ?= dev

# Colors for output
BLUE := \033[34m
GREEN := \033[32m
RED := \033[31m
RESET := \033[0m

help: ## Show this help message
	@echo "$(BLUE)EKart Store - Available Commands$(RESET)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-15s$(RESET) %s\n", $$1, $$2}'

install: ## Install all dependencies
	@echo "$(BLUE)Installing dependencies...$(RESET)"
	# Backend dependencies
	cd backend && pip install -r requirements.txt
	# Frontend dependencies
	cd frontend && npm install
	# Lambda dependencies
	cd lambda-functions/order-processor && pip install -r requirements.txt
	cd lambda-functions/inventory-updater && pip install -r requirements.txt
	cd lambda-functions/payment-processor && pip install -r requirements.txt
	cd lambda-functions/notification-sender && pip install -r requirements.txt
	@echo "$(GREEN)Dependencies installed successfully!$(RESET)"

start: ## Start all services (LocalStack, Backend, Frontend)
	@echo "$(BLUE)Starting EKart Store...$(RESET)"
	# Start LocalStack
	docker-compose up -d localstack
	# Wait for LocalStack to be ready
	./scripts/wait-for-localstack.sh
	# Deploy infrastructure
	make deploy-infra
	# Start backend
	cd backend && uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
	# Start frontend
	cd frontend && npm run dev &
	@echo "$(GREEN)All services started!$(RESET)"
	@echo "Frontend: http://localhost:3000"
	@echo "Backend API: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/api/docs"

stop: ## Stop all services
	@echo "$(BLUE)Stopping services...$(RESET)"
	docker-compose down
	pkill -f "uvicorn main:app" || true
	pkill -f "npm run dev" || true
	@echo "$(GREEN)All services stopped!$(RESET)"

restart: stop start ## Restart all services

ready: ## Check if all services are ready
	@echo "$(BLUE)Checking service health...$(RESET)"
	# Check LocalStack
	curl -s http://localhost:4566/_localstack/health | jq . || echo "$(RED)LocalStack not ready$(RESET)"
	# Check Backend
	curl -s http://localhost:8000/health | jq . || echo "$(RED)Backend not ready$(RESET)"
	# Check Frontend
	curl -s http://localhost:3000 > /dev/null && echo "$(GREEN)Frontend ready$(RESET)" || echo "$(RED)Frontend not ready$(RESET)"

logs: ## Show logs from all services
	docker-compose logs -f localstack &
	tail -f backend/app.log &
	wait

test: ## Run all tests
	@echo "$(BLUE)Running tests...$(RESET)"
	# Backend tests
	cd backend && python -m pytest tests/ -v
	# Frontend tests
	cd frontend && npm run test
	# Integration tests
	python scripts/test-integration.py
	@echo "$(GREEN)All tests completed!$(RESET)"

test-ci: ## Run tests in CI mode
	@echo "$(BLUE)Running CI tests...$(RESET)"
	cd backend && python -m pytest tests/ -v --junitxml=test-results.xml
	cd frontend && npm run test:ci
	python scripts/test-integration.py --ci

build: ## Build all components
	@echo "$(BLUE)Building components...$(RESET)"
	# Build backend Docker image
	cd backend && docker build -t ekart-backend:latest .
	# Build frontend
	cd frontend && npm run build
	# Build Lambda functions
	cd lambda-functions/order-processor && docker build -t ekart-lambda-order-processor:latest .
	cd lambda-functions/inventory-updater && docker build -t ekart-lambda-inventory-updater:latest .
	cd lambda-functions/payment-processor && docker build -t ekart-lambda-payment-processor:latest .
	cd lambda-functions/notification-sender && docker build -t ekart-lambda-notification-sender:latest .
	@echo "$(GREEN)Build completed!$(RESET)"

deploy-infra: ## Deploy infrastructure to LocalStack
	@echo "$(BLUE)Deploying infrastructure...$(RESET)"
	# Deploy CloudFormation stacks
	aws --endpoint-url=http://localhost:4566 cloudformation deploy \
		--template-file infrastructure/cloudformation/main.yml \
		--stack-name ekart-$(ENV) \
		--parameter-overrides Environment=$(ENV) \
		--capabilities CAPABILITY_IAM
	# Deploy Lambda functions
	./scripts/deploy-lambdas.sh
	@echo "$(GREEN)Infrastructure deployed!$(RESET)"

seed-data: ## Seed database with sample data
	@echo "$(BLUE)Seeding database...$(RESET)"
	python scripts/seed-data.py
	@echo "$(GREEN)Database seeded!$(RESET)"

clean: ## Clean up containers, images, and build artifacts
	@echo "$(BLUE)Cleaning up...$(RESET)"
	docker-compose down -v --remove-orphans
	docker system prune -f
	cd backend && rm -rf __pycache__ .pytest_cache
	cd frontend && rm -rf .next node_modules/.cache
	@echo "$(GREEN)Cleanup completed!$(RESET)"

dev-setup: install deploy-infra seed-data ## Complete development setup
	@echo "$(GREEN)Development environment ready!$(RESET)"
	@echo "Run 'make start' to begin development"

monitor: ## Open monitoring dashboard
	@echo "$(BLUE)Opening monitoring dashboard...$(RESET)"
	open http://localhost:4566/_localstack/cockpit || xdg-open http://localhost:4566/_localstack/cockpit

# Environment-specific targets
dev: ENV := dev
dev: dev-setup ## Setup development environment

staging: ENV := staging
staging: build deploy-infra ## Deploy to staging

production: ENV := prod
production: build deploy-infra ## Deploy to production

# Docker compose shortcuts
up: ## Start services with docker-compose
	docker-compose up -d

down: ## Stop services with docker-compose
	docker-compose down

ps: ## Show running containers
	docker-compose ps

# Utility targets
backend-shell: ## Open backend shell
	cd backend && python -c "from main import app; import IPython; IPython.embed()"

frontend-shell: ## Open frontend Node.js REPL
	cd frontend && npx ts-node

aws-shell: ## Open AWS CLI with LocalStack endpoint
	aws --endpoint-url=http://localhost:4566 s3 ls

format: ## Format code
	cd backend && black . && isort .
	cd frontend && npm run format

lint: ## Lint code
	cd backend && flake8 . && mypy .
	cd frontend && npm run lint

docs: ## Generate documentation
	cd backend && pdoc --html --output-dir docs .
	cd frontend && npm run build-docs

backup: ## Backup LocalStack data
	docker-compose exec localstack ls -la /tmp/localstack
	docker cp $$(docker-compose ps -q localstack):/tmp/localstack ./backup-$$(date +%Y%m%d_%H%M%S)
