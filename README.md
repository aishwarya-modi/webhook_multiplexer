# Webhook Multiplexer Service

This is a webhook multiplexer service built using Flask and MongoDB. The service acts as an intermediary between SaaS products and customer endpoints, allowing customers to create custom webhook endpoints and forward incoming webhooks to multiple destinations.

## Features

- **Receive Webhooks**: Accept incoming webhooks from various SaaS products.
- **Store Webhooks**: Store webhook configurations and logs in MongoDB.
- **Forward Webhooks**: Forward the incoming webhook payloads to multiple customer-defined endpoints.
- **API Documentation**: Interactive API documentation with Swagger.
- **Error Handling**: Comprehensive error handling for database and other errors.

## Prerequisites

- Python 3.6+
- MongoDB

## Installation

1. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt

2. **Set up environment variables**:
  Create a .env file in the project root with the following content:
  ```bash
  MONGO_URI=mongodb://localhost:27017/webhook_mux
  SECRET_KEY=your_secret_key
  ```

3.  **Run the MongoDB server**:
  ```bash
  mongod --dbpath /path/to/your/mongodb/data
```

4. **Start the Flask application**:
  ```bash
  python app.py
```

5. **Access the API documentation**:

On the browser navigate to http://localhost:5000/apidocs to view the interactive API documentation.
