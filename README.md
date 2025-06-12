# Address Book Service

A modular, high-performance address book service with in-memory storage designed to scale to millions of contacts. Built with Python Flask and optimized for O(1) operations.

## Features

- **High Performance**: O(1) time complexity for search, create, update, and delete operations
- **Modular Architecture**: Clean separation of concerns across models, storage, services, and controllers
- **In-Memory Storage**: Fast access with multiple indexes for efficient searching
- **Thread-Safe**: Concurrent request handling with proper synchronization
- **RESTful API**: Well-defined JSON API following standard HTTP conventions
- **Extensible Design**: Easy to add new features and functionality

## Architecture

```
├── models/           # Data models (Contact)
├── storage/          # In-memory storage layer with indexes
├── services/         # Business logic layer
├── controllers/      # API controllers and request handling
├── app.py           # Main Flask application
└── requirements.txt # Python dependencies
```

### Layer Responsibilities

- **Models**: Define data structure and validation
- **Storage**: In-memory data persistence with optimized indexes
- **Services**: Business logic, validation, and orchestration
- **Controllers**: HTTP request/response handling and routing

## Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation & Setup

1. **Clone or navigate to the project directory**
   ```bash
   cd address_book
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Verify the service is running**
   ```bash
   curl http://localhost:5000/health
   ```

The service will be available at `http://localhost:5000`

## API Documentation

### Base URL
```
http://localhost:5000
```

### Endpoints

#### 1. Create Contacts
**POST** `/create`

Create one or more contacts.

**Request Body:**
```json
[
  {
    "name": "Alice Smith",
    "phone": "1234567890",
    "email": "alice@example.com"
  },
  {
    "name": "Bob Jones", 
    "phone": "2345678901",
    "email": "bob@example.com"
  }
]
```

**Response:**
```json
[
  {
    "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "name": "Alice Smith",
    "phone": "1234567890", 
    "email": "alice@example.com"
  },
  {
    "id": "e3b0c442-98fc-1c14-9af5-abc12d3e4d59",
    "name": "Bob Jones",
    "phone": "2345678901",
    "email": "bob@example.com"
  }
]
```

#### 2. Update Contacts
**PUT** `/update`

Update one or more contacts by ID.

**Request Body:**
```json
[
  {
    "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "phone": "9999999999"
  },
  {
    "id": "e3b0c442-98fc-1c14-9af5-abc12d3e4d59", 
    "email": "newbob@example.com"
  }
]
```

**Response:**
```json
[
  {
    "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "name": "Alice Smith",
    "phone": "9999999999",
    "email": "alice@example.com"
  },
  {
    "id": "e3b0c442-98fc-1c14-9af5-abc12d3e4d59",
    "name": "Bob Jones", 
    "phone": "2345678901",
    "email": "newbob@example.com"
  }
]
```

#### 3. Delete Contacts
**DELETE** `/delete`

Delete one or more contacts by ID.

**Request Body:**
```json
[
  "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "e3b0c442-98fc-1c14-9af5-abc12d3e4d59"
]
```

**Response:**
```json
{
  "deleted": 2
}
```

#### 4. Search Contacts
**POST** `/search`

Search contacts by query string. Searches across name, phone, and email fields.

**Request Body:**
```json
{
  "query": "Smith"
}
```

**Response:**
```json
[
  {
    "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "name": "Alice Smith",
    "phone": "1234567890",
    "email": "alice@example.com"
  },
  {
    "id": "c76b5cda-7122-45c4-9a10-df0a312bc9fe",
    "name": "Charlie Smith",
    "phone": "3456789012", 
    "email": "charlie@example.com"
  }
]
```

#### 5. Health Check
**GET** `/health`

Check service health status.

**Response:**
```json
{
  "status": "healthy",
  "service": "Address Book API",
  "version": "1.0.0"
}
```

## Usage Examples

### Using curl

1. **Create contacts:**
   ```bash
   curl -X POST http://localhost:5000/create \
     -H "Content-Type: application/json" \
     -d '[{"name": "John Doe", "phone": "1234567890", "email": "john@example.com"}]'
   ```

2. **Search contacts:**
   ```bash
   curl -X POST http://localhost:5000/search \
     -H "Content-Type: application/json" \
     -d '{"query": "John"}'
   ```

3. **Update contact:**
   ```bash
   curl -X PUT http://localhost:5000/update \
     -H "Content-Type: application/json" \
     -d '[{"id": "YOUR_CONTACT_ID", "phone": "9876543210"}]'
   ```

4. **Delete contacts:**
   ```bash
   curl -X DELETE http://localhost:5000/delete \
     -H "Content-Type: application/json" \
     -d '["YOUR_CONTACT_ID"]'
   ```

## Performance Characteristics

- **Create**: O(1) - Hash map insertion with index updates
- **Read**: O(1) - Direct hash map lookup by ID
- **Update**: O(1) - Hash map update with index refresh
- **Delete**: O(1) - Hash map deletion with index cleanup
- **Search**: O(k) where k is the number of matching contacts

## Data Storage

The service uses an optimized in-memory storage system with multiple indexes:

- **Primary Index**: `contact_id → Contact` (hash map)
- **Name Index**: `name_word → Set[contact_id]` (inverted index)
- **Phone Index**: `phone → contact_id` (hash map)  
- **Email Index**: `email → contact_id` (hash map)

This design ensures fast lookups while maintaining data consistency.

## Thread Safety

The service is designed for concurrent access:
- Thread-safe storage operations using `threading.RLock()`
- Atomic operations for data consistency
- Safe for multiple simultaneous requests

## Error Handling

The API returns appropriate HTTP status codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request (validation errors)
- `404`: Not Found
- `405`: Method Not Allowed
- `500`: Internal Server Error

## Extensibility

The modular architecture makes it easy to extend:
- Add new contact fields by updating the `Contact` model
- Implement additional storage backends by extending the storage interface
- Add new API endpoints in the controller layer
- Integrate external services in the service layer

## Development

### Project Structure
```
address_book/
├── models/
│   ├── __init__.py
│   └── contact.py
├── storage/
│   ├── __init__.py
│   └── memory_store.py
├── services/
│   ├── __init__.py
│   └── contact_service.py
├── controllers/
│   ├── __init__.py
│   └── contact_controller.py
├── app.py
├── requirements.txt
└── README.md
```

### Key Design Decisions

1. **UUID Generation**: RFC 4122 compliant UUIDs for unique identification
2. **Index Strategy**: Multiple specialized indexes for different search patterns
3. **Modular Design**: Clear separation enabling independent testing and development
4. **Flask Framework**: Lightweight, well-documented, and widely adopted
5. **In-Memory Storage**: Fastest possible access without external dependencies

## License

This project is available for educational and demonstration purposes. 