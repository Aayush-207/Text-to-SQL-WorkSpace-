"""Quick start guide."""
# 🚀 Quick Start Guide

## Prerequisites

- Python 3.12+
- PostgreSQL 14+
- Gemini API Key

## 1️⃣ Setup

### Option A: Local Development

```bash
# Clone repository
git clone <repo-url>
cd Text-to-SQL-WorkSpace-

# Create Python virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
```

### Option B: Docker (Recommended)

```bash
# Docker Compose setup
docker-compose up -d
```

## 2️⃣ Configuration

### Local Development

```bash
# Copy environment template
cp backend/.env.example backend/.env

# Edit .env with your settings
```

**Required variables:**
```env
GEMINI_API_KEY=your-api-key-here
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=password
```

### Docker

Environment in `docker-compose.yml`:
```yaml
environment:
  GEMINI_API_KEY: ${GEMINI_API_KEY}  # Pass from host
  DB_HOST: postgres
  DB_PASSWORD: password
```

## 3️⃣ Database Setup

### Option A: psql

```bash
# Create database
createdb -U postgres postgres

# Load sample data
psql -U postgres postgres < init-db.sql
```

### Option B: Docker

Database auto-initializes with `init-db.sql`

## 4️⃣ Start Server

### Local

```bash
cd backend
uvicorn app.main:app --reload

# Server at http://localhost:8000
```

### Docker

```bash
docker-compose up -d

# Logs
docker-compose logs -f backend
```

## 5️⃣ Test API

### Health Check

```bash
curl http://localhost:8000/health
```

### Generate SQL

```bash
curl -X POST "http://localhost:8000/api/v1/generate/sql" \
  -H "Content-Type: application/json" \
  -d '{
    "natural_language_query": "Get all users",
    "schema": "public"
  }'
```

### View Docs

- Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🎯 Common Tasks

### Install Packages

```bash
pip install -r backend/requirements.txt
```

### Run Tests

```bash
pytest backend/tests
```

### Format Code

```bash
make format
```

### View Logs

```bash
# Docker
docker-compose logs -f backend

# Local (JSON format to stdout)
```

### Access Database

```bash
# Docker
docker-compose exec postgres psql -U postgres

# Local
psql -U postgres postgres
```

## 🛠️ Troubleshooting

### Database Connection Failed

```bash
# Check PostgreSQL is running
psql -U postgres -c "SELECT 1"

# Check .env settings
cat backend/.env
```

### API Not Starting

```bash
# Check dependencies
pip list | grep fastapi

# Check port 8000 is free
netstat -an | grep 8000

# Check logs
docker-compose logs backend
```

### Gemini API Error

```bash
# Verify API key
echo $GEMINI_API_KEY

# Check quota at: https://console.cloud.google.com
```

## 📚 Next Steps

1. ✅ Explore API documentation: `/docs`
2. 📖 Read [Backend README](backend/README.md)
3. 🚀 Deploy to production
4. 🧪 Write tests for your use case

## 🆘 Getting Help

- Check API docs: `http://localhost:8000/docs`
- Review logs in JSON format
- Check configuration in `.env`
- See [Backend README](backend/README.md) for details
