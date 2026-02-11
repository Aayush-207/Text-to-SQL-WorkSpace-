"""Backend README."""
# Text to SQL API - Backend

AI-powered SQL generator backend using FastAPI and Gemini.

## 🚀 Features

### 1️⃣ Metadata Extraction
- Extract schema from PostgreSQL databases
- Query `information_schema` for complete metadata
- Fetch foreign key relationships
- Return structured JSON responses

### 2️⃣ SQL Validator
- 🚫 Block dangerous operations: DROP DATABASE, TRUNCATE
- 🚫 Block multiple statements in single query
- ✅ Require WHERE clause for DELETE statements
- ✅ Inject LIMIT 100 for SELECT queries (configurable)
- 🛡️ Security-first validation

### 3️⃣ Preview Engine
- Convert UPDATE/DELETE to SELECT for preview
- Show affected rows before execution
- Transaction-safe execution
- Rollback on failure

### 4️⃣ Transaction System
- Wrap write queries in BEGIN/COMMIT
- Automatic rollback on error
- Connection pooling
- Async database operations

### 5️⃣ Gemini Integration
- Structured JSON output:
  ```json
  {
    "sql": "SELECT * FROM users WHERE id = 1",
    "type": "SELECT",
    "confidence": 0.95,
    "explanation": "Fetches user with ID 1"
  }
  ```
- No free text responses
- Temperature-controlled generation
- Context-aware SQL generation

## 📋 Requirements

- Python 3.12+
- PostgreSQL 14+
- Gemini API Key

## 🛠️ Installation

### 1. Clone and Setup

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy and edit .env file
cp .env.example .env
```

Set your values:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=password
GEMINI_API_KEY=your-gemini-api-key
DEBUG=false
```

### 4. Database Setup

```bash
# Create PostgreSQL database
createdb -U postgres postgres

# Load sample data
psql -U postgres postgres < ../init-db.sql
```

## 🚀 Running

### Development

```bash
uvicorn app.main:app --reload
```

Server runs at: `http://localhost:8000`

### Production

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

## 🐳 Docker

```bash
# Build
docker build -f backend/Dockerfile -t text-to-sql-backend .

# Run with compose
docker-compose up -d
```

## 📚 API Endpoints

### Connection
- `POST /api/v1/connect/test` - Test database connection
- `GET /api/v1/connect/status` - Get connection status

### Schema
- `GET /api/v1/schema/metadata` - Get complete schema
- `GET /api/v1/schema/tables` - List tables
- `GET /api/v1/schema/columns` - Get columns
- `GET /api/v1/schema/foreign-keys` - Get relationships
- `GET /api/v1/schema/sample-data` - Get sample data

### SQL Generation
- `POST /api/v1/generate/sql` - Generate SQL from natural language

### Preview
- `POST /api/v1/preview/execute` - Preview query
- `POST /api/v1/preview/simulate` - Simulate execution

### Execution
- `POST /api/v1/execute/query` - Execute query
- `POST /api/v1/execute/batch` - Execute multiple queries
- `POST /api/v1/execute/explain` - Explain query

### History
- `GET /api/v1/history/queries` - Query history
- `GET /api/v1/history/statistics` - Statistics

## 📖 API Documentation

### Auto-Generated Docs
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Example: Generate SQL

```bash
curl -X POST "http://localhost:8000/api/v1/generate/sql" \
  -H "Content-Type: application/json" \
  -d '{
    "natural_language_query": "Get all users from California",
    "schema": "public"
  }'
```

### Example: Execute Query

```bash
curl -X POST "http://localhost:8000/api/v1/execute/query" \
  -H "Content-Type: application/json" \
  -d '{
    "sql": "SELECT * FROM users LIMIT 100"
  }'
```

## 🔒 Security Features

- SQL injection prevention via parameterized queries
- Dangerous operation blocking
- Transaction safety with rollback
- Authentication-ready (JWT setup)
- CORS configured
- Structured logging

## 📊 Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── connect.py
│   │   │   ├── schema.py
│   │   │   ├── generate_sql.py
│   │   │   ├── preview.py
│   │   │   ├── execute.py
│   │   │   └── history.py
│   ├── db/
│   │   ├── connection_manager.py
│   │   ├── metadata_service.py
│   │   ├── query_validator.py
│   │   ├── query_executor.py
│   │   └── transaction_manager.py
│   ├── ai/
│   │   ├── prompt_builder.py
│   │   ├── sql_generator.py
│   │   ├── sql_explainer.py
│   │   └── optimizer.py
│   ├── services/
│   │   ├── preview_service.py
│   │   ├── diff_service.py
│   │   └── chart_service.py
│   ├── models/
│   │   └── schemas.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── utils/
│   │   └── logger.py
│   └── main.py
├── requirements.txt
├── .env
└── Dockerfile
```

## 🧪 Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov

# Specific test
pytest tests/test_query_validator.py
```

## 📝 Logging

All operations logged to stdout in JSON format:

```json
{
  "timestamp": "2024-02-10T10:30:45.123456",
  "level": "INFO",
  "logger": "text_to_sql",
  "message": "Query validated successfully: SELECT"
}
```

## 🚨 Error Handling

All errors return structured JSON:

```json
{
  "success": false,
  "error": "Error message",
  "detail": "Additional details"
}
```

## 🔄 Workflow

1. **User Input** → Natural language question
2. **Schema Extraction** → Get database metadata
3. **AI Generation** → Use Gemini to generate SQL
4. **Validation** → Security checks
5. **Preview** → Show affected rows
6. **Execute** → Run with transaction safety
7. **Return Results** → JSON response

## 🤝 Contributing

1. Code style: Black, isort
2. Type hints required
3. Docstrings for all functions
4. Tests required for new features

## 📄 License

MIT License

## 🆘 Support

For issues and questions:
- Check API docs at `/docs`
- Review logs in JSON format
- Check configuration in `.env`
