# Text to SQL - AI-Powered SQL Generator

Generate SQL queries from natural language using Gemini AI with PostgreSQL.

## 🎯 Overview

Transform natural language questions into production-ready SQL queries.

## 🚀 Quick Start

### Docker (Recommended)
```bash
docker-compose up -d
```

### Local Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
cd backend && uvicorn app.main:app --reload
```

Visit: http://localhost:8000/docs

## 📚 Documentation

- [Quick Start Guide](./QUICKSTART.md)
- [Backend Documentation](./backend/README.md)
- [API Reference](./backend/README.md)

## 🔒 Security

✅ Block DROP DATABASE / TRUNCATE  
✅ Require WHERE for DELETE  
✅ Transaction safety  

## 📄 License

MIT License