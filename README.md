# FastAPI Ecommerce Backend

A comprehensive ecommerce backend API built with FastAPI and MongoDB, following clean architecture principles.

## Features

- **Product Management**: Create and list products with filtering and pagination
- **Order Management**: Create orders and retrieve user order history
- **Clean Architecture**: Follows MVC pattern with proper separation of concerns
- **Error Handling**: Comprehensive error handling with custom exceptions
- **Logging**: Structured logging throughout the application


## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **MongoDB**: NoSQL database with Motor (async driver)
- **Pydantic**: Data validation and settings management
- **Python 3.10+**: Modern Python features

## Project Structure

```
app/
├── api/
│   └── v1/
│       ├── endpoints/
│       │   ├── products.py      # Product endpoints
│       │   └── orders.py        # Order endpoints
│       └── router.py            # Main API router
├── core/
│   ├── config.py               # Application configuration
│   ├── database.py             # Database connection
│   ├── exceptions.py           # Custom exceptions
│   └── logging_config.py       # Logging setup
├── models/
│   ├── product.py              # Product schemas
│   └── order.py                # Order schemas
├── repositories/
│   ├── product_repository.py   # Product data access
│   └── order_repository.py     # Order data access
└── services/
    ├── product_service.py      # Product business logic
    └── order_service.py        # Order business logic
```

## API Endpoints

### Products

- `POST /products` - Create a new product
- `GET /products` - List products with filtering and pagination

### Orders

- `POST /orders` - Create a new order
- `GET /orders/{user_id}` - Get user orders with pagination

## Setup Instructions

1. **Clone the Repository**
   ```
   git clone https://github.com/AbhimanyuAhuja12/HRone-Ecommerce-Backend/
   ```

2. **Install Dependencies**
   ```
   pip install -r requirements.txt
   ```

3. **Setup MongoDB**
   - Install MongoDB locally or use MongoDB Atlas
   - Copy `.env.example` to `.env` and update connection string

4. **Seed Database (Optional)**
   ```
   python scripts/seed_data.py
   ```

5. **Run Application**
   ```
   uvicorn main:app --reload
   ```

6. **Access API Documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Environment Variables

```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=ecommerce_db
DEBUG=false
LOG_LEVEL=INFO
```

## API Usage Examples

### Create Product
```
curl -X POST "http://localhost:8000/products" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sample Product",
    "price": 99.99,
    "sizes": [
      {"size": "medium", "quantity": 10},
      {"size": "large", "quantity": 5}
    ]
  }'
```

### List Products
```
curl "http://localhost:8000/products?name=shirt&size=large&limit=10&offset=0"
```

### Create Order
```
curl -X POST "http://localhost:8000/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "user_123",
    "items": [
      {"productId": "product_id_here", "qty": 2}
    ]
  }'
```

### Get User Orders
```
curl "http://localhost:8000/orders/user_123?limit=10&offset=0"
```

