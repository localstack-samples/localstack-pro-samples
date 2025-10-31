"# EKart Store Architecture

## Overview
This document describes the architecture of the EKart Store e-commerce platform, with a focus on the recent fixes for order processing workflow.

## Components

### Frontend (Next.js)
- Server-side rendered React application
- TypeScript for type safety
- Tailwind CSS for styling
- Three.js for 3D product visualization

### Backend (FastAPI)
- RESTful API built with Python FastAPI
- Pydantic models for data validation
- JWT authentication via AWS Cognito
- Integration with AWS services via boto3

### Infrastructure (AWS via LocalStack)
- **DynamoDB**: NoSQL database for all entities
- **S3**: Object storage for product images
- **Cognito**: User authentication and authorization
- **Lambda**: Serverless functions for async processing
- **API Gateway**: RESTful API endpoints
- **SQS**: Message queues for order processing
- **EventBridge**: Event-driven architecture
- **SES**: Transactional email delivery

## Data Flow

### Fixed Order Processing Workflow
1. User adds items to cart via Frontend → Cart API
2. User proceeds to checkout with shipping information
3. Frontend calls Payment API to create payment intent
4. After payment confirmation, Frontend calls Payment API to confirm payment
5. **FIXED**: Payment Processor now creates orders in DynamoDB and links them to payment intents
6. Orders are now visible in the Orders API
7. Lambda functions process async tasks like notifications
8. SES sends email notifications

### Database Schema

#### Orders Table (ekart-orders-dev)
- Primary Key: order_id
- GSI: buyer_id (for buyer order lookup)
- GSI: seller_id (for seller order lookup)
- Fields: items, total_amount, status, payment_status, shipping_address, timestamps

#### Products Table (ekart-products-dev)
- Primary Key: product_id
- GSI: seller_id (for seller product management)
- GSI: category (for category browsing)
- Fields: title, description, price, stock_quantity, images

#### Carts Table (ekart-carts-dev)
- Primary Key: user_id
- Fields: items, timestamps

## Security

- All API endpoints require JWT authentication
- S3 buckets have private access control
- Cognito manages user credentials
- HTTPS enforced in production

## Recent Fixes

### Order Visibility Issue
**Problem**: Orders were not appearing in the orders list after successful payment.

**Root Cause**: The payment processing workflow was not properly integrated with order creation. Payment intents were created but orders were never actually stored in the database.

**Solution**: Enhanced the payment processor Lambda function to:
1. Create payment intents as before
2. Upon payment confirmation, create actual orders in DynamoDB
3. Link payment intents to orders for proper tracking
4. Update order status when payment status changes

**Impact**: Orders now properly appear in the orders list immediately after successful payment."