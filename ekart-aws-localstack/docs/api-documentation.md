"# EKart Store API Documentation

## Base URL
- Local: `http://localhost:8000/api`
- Production: `https://api.ekart.com/api`

## Authentication
All protected endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <token>
```

## Endpoints

### Products

#### GET /products
Get all products with optional filters
- Query params: category, min_price, max_price, brand, seller_id, page, per_page
- Response: Array of products

#### GET /products/{id}
Get a specific product by ID
- Response: Product object

#### POST /products
Create a new product (sellers only)
- Request body: ProductCreate
- Response: Created product

#### PUT /products/{id}
Update a product (owner only)
- Request body: ProductUpdate
- Response: Updated product

#### DELETE /products/{id}
Delete a product (owner only)
- Response: Success message

### Orders

#### GET /orders
Get user's orders
- Response: Array of orders

#### GET /orders/{id}
Get a specific order by ID
- Response: Order object

#### POST /orders
Create a new order from cart
- Request body: ShippingAddress, PaymentMethod
- Response: Created order(s)

#### PUT /orders/{id}/status
Update order status (sellers only)
- Request body: Status update
- Response: Updated order

### Cart

#### GET /cart
Get user's shopping cart
- Response: Cart object with items

#### POST /cart/items
Add item to cart
- Request body: CartItem
- Response: Updated cart

#### PUT /cart/items/{product_id}
Update item quantity in cart
- Request body: Quantity
- Response: Updated cart

#### DELETE /cart/items/{product_id}
Remove item from cart
- Response: Updated cart

### Payments

#### POST /payments/create-payment-intent
Create a payment intent for checkout
- Request body: Amount, Currency, Metadata
- Response: PaymentIntent details

#### POST /payments/confirm-payment
Confirm payment and create order
- Request body: PaymentIntent ID, ShippingAddress
- Response: Confirmation and order details

#### GET /payments/payment-intent/{id}
Get payment intent details
- Response: PaymentIntent object

### Authentication

#### POST /auth/register
Register a new user
- Request body: UserCreate
- Response: User profile + token

#### POST /auth/login
Login with email and password
- Request body: UserLogin
- Response: User profile + token

## Data Models

### Order
```json
{
  \"order_id\": \"string\",
  \"buyer_id\": \"string\",
  \"seller_id\": \"string\",
  \"items\": [OrderItem],
  \"total_amount\": \"number\",
  \"status\": \"pending|confirmed|processing|shipped|delivered|cancelled\",
  \"payment_status\": \"pending|completed|failed\",
  \"payment_method\": \"card|paypal|wallet|cod\",
  \"shipping_address\": ShippingAddress,
  \"created_at\": \"datetime\",
  \"updated_at\": \"datetime\"
}
```

### Product
```json
{
  \"product_id\": \"string\",
  \"seller_id\": \"string\",
  \"title\": \"string\",
  \"description\": \"string\",
  \"price\": \"number\",
  \"category\": \"string\",
  \"stock_quantity\": \"integer\",
  \"images\": [\"string\"],
  \"is_active\": \"boolean\",
  \"created_at\": \"datetime\",
  \"updated_at\": \"datetime\"
}
```

## Error Responses

All endpoints return standard HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error"