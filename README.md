# Lyftr AI — Backend Assignment

Hi! 👋 This is my submission for the **Lyftr AI Backend Assignment**.

I have designed and implemented a production-ready, asynchronous ingestion API using **FastAPI** and **SQLite**, strictly adhering to the specified constraints.

## 📋 Project Overview

This service acts as a high-throughput webhook receiver and message store. It is designed to be:
- **Robust**: Validates HMAC signatures for security and enforces strict deduplication.
- **Observable**: Exposes health checks (`/health`) and Prometheus metrics (`/metrics`).
- **Maintainable**: Uses a clean, modular structure with strictly typed Pydantic models.
- **Portable**: Fully containerized with Docker, requiring no external dependencies.

### Constraints & Compliance
This solution was built with the following strict requirements in mind:
- **No external services**: Database is **SQLite** (file-based).
- **Environment Configuration**: All secrets and settings are loaded via environment variables (12-factor app).
- **Exact Semantics**:
    - **Deduplication**: Messages are ignored if `text` + `timestamp` match an existing entry.
    - **Security**: `X-Signature` header is validated using HMAC-SHA256.

*Setup Used: VSCode + AI Assistant (for boilerplate & testing patterns).*

## 🚀 Features

### 1. Ingestion (`POST /webhook`)
- Accepting WhatsApp-like message payloads.
- **Security**: Verifies `X-Signature` header against `WEBHOOK_SECRET` using HMAC-SHA256.
- **Idempotency**: Implements strict deduplication logic. If a message with the same body and timestamp arrives twice, the second one is acknowledged (200 OK) but not stored.

### 2. Retrieval (`GET /messages`)
- Fetch stored messages with pagination (`limit`, `offset`).
- Supports filtering by sender (`from` query parameter).
- Returns a structured JSON response containing total counts and metadata.

### 3. Analytics (`GET /stats`)
- Provides quick insights into the system usage.
- Returns total message count, messages in the last 24 hours, and the top sender.

### 4. Observability
- **`GET /health`**: Simple liveness/readiness probe for Kubernetes/orchestrators.
- **`GET /metrics`**: Prometheus-formatted metrics including request latency and counts.

## 🛠️ Tech Stack

- **Python 3.10+**: Core language.
- **FastAPI**: Modern, high-performance web framework.
- **SQLAlchemy (Async)** + **aiosqlite**: For non-blocking database operations.
- **Pydantic**: For strict data validation and serialization.
- **Docker & Docker Compose**: For containerization and easy deployment.

## 🏃‍♂️ How to Run

### Using Docker (Recommended)
This approach guarantees the environment matches the one used during development and testing.

1. **Build and Start**:
   ```bash
   docker-compose up --build
   ```
2. **Access Endpoints**:
   - API Docs: `http://localhost:8000/docs`
   - Health Check: `http://localhost:8000/health`

### Local Development
If you wish to run it locally (requires Python 3.10+):

1. **Setup Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Run Server**:
   ```bash
   export WEBHOOK_SECRET=your_super_secret_key_change_me
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

## 🧪 Verification

I have included a strictly defined test suite using `pytest` to verify correctness.

To run the tests inside the container:
```bash
docker-compose run --rm api pytest tests/ -v
```

All tests pass, confirming:
- ✅ Correct HMAC validation.
- ✅ Strict deduplication logic.
- ✅ Pagination and filtering behavior.
- ✅ Stats calculation.

---
*Submitted by [Your Name]*
