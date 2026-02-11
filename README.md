# Text to SQL - Full-Stack AI-Powered Database Query Tool

A production-ready full-stack application that converts natural language to SQL queries using Google's Gemini AI. Features a FastAPI backend with async PostgreSQL support and a modern React Vite frontend.

## Project Overview

**Text to SQL** enables users to:
1. Connect to PostgreSQL databases with credentials
2. Automatically fetch and display database schema
3. Enter natural language prompts
4. Convert prompts → SQL using Gemini AI
5. Validate SQL before execution
6. Support Safe Mode (SELECT only) and Edit Mode
7. Preview affected rows before executing writes
8. Execute with transaction-based safety
9. Display results in table or chart formats
10. Maintain complete query history

## Quick Start

### Prerequisites
- Docker & Docker Compose (recommended)
- Google Gemini API Key

### Docker Compose (Recommended)

```bash
cd "Text to SQL workspace"
export GOOGLE_API_KEY=your_gemini_api_key
docker-compose up

# Frontend: http://localhost:5173
# Backend: http://localhost:8000/docs
```

### Local Development

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export GOOGLE_API_KEY=your_gemini_api_key
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Project Structure

- **backend/** - FastAPI backend (40+ Python files)
- **frontend/** - React Vite frontend (16+ TypeScript files)
- **docker-compose.yml** - Complete stack orchestration

## Key Features

**Backend (5 Core Components)**
✓ Async PostgreSQL connection management
✓ Automatic schema metadata extraction
✓ SQL validation with security scanning
✓ Safe query preview engine
✓ Gemini AI SQL generation

**Frontend (8 React Components)**
✓ DatabaseConnector - Connection form
✓ SchemaViewer - Schema browser
✓ ChatPanel - Natural language input
✓ QueryEditor - SQL editor
✓ ResultTable - Paginated results
✓ ChartViewer - Auto-detect visualizations
✓ ConfirmationModal - Safe execution
✓ QueryHistory - Query tracking

**Full-Stack Features**
✓ Natural language to SQL conversion
✓ Safe Mode (SELECT) + Edit Mode (all queries)
✓ Query preview with affected row counts
✓ Transaction-based execution
✓ Table & chart visualization
✓ TypeScript throughout

## Security

- SQL injection prevention
- Dangerous operation blocking (DROP, TRUNCATE)
- Transaction ACID compliance
- Parameterized queries

## Documentation

- [Backend README](backend/README.md) - API docs, deployment
- [Frontend README](frontend/README.md) - Components, setup
- [Frontend SETUP](frontend/SETUP.md) - Deployment guide

## Tech Stack

- **Backend**: Python FastAPI + SQLAlchemy + asyncpg
- **Frontend**: React 18 + TypeScript + Vite + TailwindCSS
- **AI**: Google Generative AI (Gemini)
- **Database**: PostgreSQL 14+
- **Deployment**: Docker & Docker Compose

**Status**: ✅ Production-Ready (40+ backend + 16+ frontend files)