# Data Ingestion Service

A service for ingesting and managing data from various partners, built using Domain-Driven Design (DDD) principles and Hexagonal Architecture.

## Architecture

This project follows a Hexagonal Architecture (Ports and Adapters) with the following layers:

- **Domain Layer**: Contains the core business logic, entities, value objects, and domain events.
- **Application Layer**: Contains application services, commands, and queries (CQS pattern).
- **Infrastructure Layer**: Contains implementations of repositories, event bus, and API endpoints.

## Domain-Driven Design Elements

The service implements the following DDD concepts:

- **Entities**: Domain objects with identity (e.g., `IngestedData`)
- **Value Objects**: Immutable objects without identity (e.g., `PartnerId`, `Payload`, `Timestamp`)
- **Aggregates**: Cluster of domain objects treated as a unit (e.g., `IngestedData` as an aggregate root)
- **Repositories**: Persistence abstractions (e.g., `DataRepository`)
- **Domain Events**: Events that represent something that happened in the domain (e.g., `DataIngested`)
- **Factories**: Objects that create complex domain objects (e.g., `IngestedDataFactory`)

## Command Query Separation (CQS)

The service uses the CQS pattern to separate operations that modify state (commands) from operations that read state (queries):

- **Commands**: `IngestDataCommand`
- **Queries**: `GetDataByIdQuery`, `GetAllDataQuery`, `GetDataByPartnerIdQuery`

## Event-Driven Communication

Communication between different modules is done through domain events:

1. When data is ingested, a `DataIngested` event is published
2. Subscribers can react to these events (e.g., logging, further processing)

## Database

The service uses SQLAlchemy for database operations, with support for:

- SQLite (default for development)

## Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL (optional, SQLite is used by default)

### Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Configure the database in `.env` file (optional)
4. Run the application:
   ```
   python main.py
   ```

### Docker

To run the service using Docker:

```
docker build -t ingestion-service .
docker run -p 5001:5001 ingestion-service
```

## API Endpoints

- `POST /ingest`: Ingest new data
- `GET /ingest/<data_id>`: Get data by ID
- `GET /ingest/partner/<partner_id>`: Get all data for a specific partner
- `GET /ingest/all`: Get all ingested data
