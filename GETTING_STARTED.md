# Getting Started - Text to SQL

## What You Have

A complete, production-ready full-stack application with:
- **Backend**: 40+ Python files (FastAPI + PostgreSQL + Gemini AI)
- **Frontend**: 30 TypeScript files (React + Vite + TailwindCSS)
- **Infrastructure**: Docker Compose setup
- **Documentation**: 10+ guide files

---

## Prerequisites

Make sure you have installed:
- Docker Desktop (recommended) or
- Node.js 16+ & Python 3.10+ & PostgreSQL 14+
- Google Gemini API Key (get from Google AI Studio)

---

## Option 1: Docker Compose (Recommended - 2 minutes)

### Step 1: Set API Key
```bash
# On macOS/Linux
export GOOGLE_API_KEY=your_gemini_api_key_here

# On Windows PowerShell
$env:GOOGLE_API_KEY="your_gemini_api_key_here"
```

### Step 2: Start Everything
```bash
cd "Text to SQL workspace"
docker-compose up
```

### Step 3: Access the Application
- **Frontend**: http://localhost:5173
- **Backend API Docs**: http://localhost:8000/docs
- **Database**: PostgreSQL on localhost:5432 (user: postgres, password: postgres)

---

## Option 2: Local Development Setup

### Backend Setup

**1. Create Virtual Environment**
```bash
cd backend
python -m venv venv

# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

**2. Install Dependencies**
```bash
pip install -r requirements.txt
```

**3. Set Environment Variable**
```bash
# On macOS/Linux
export GOOGLE_API_KEY=your_gemini_api_key_here
export DATABASE_URL=postgresql://user:password@localhost:5432/postgres

# On Windows PowerShell
$env:GOOGLE_API_KEY="your_gemini_api_key_here"
$env:DATABASE_URL="postgresql://user:password@localhost:5432/postgres"
```

**4. Start Backend**
```bash
uvicorn app.main:app --reload --port 8000
```

Visit: http://localhost:8000/docs for interactive API documentation

### Frontend Setup

**In a new terminal window:**

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The app will open at http://localhost:5173

---

## First Steps

### 1. Connect to Database
1. On the application, fill in database credentials:
   - Host: `localhost`
   - Port: `5432`
   - Database: `postgres`
   - User: `postgres`
   - Password: `postgres` (or your actual password)
2. Click "Connect"

### 2. Browse Schema
Once connected, you'll see the database schema in the left panel

### 3. Generate SQL
Try entering a natural language query like:
- "Show me all tables"
- "Get user count"
- "List orders from last month"

### 4. Execute & Visualize
See the generated SQL, preview results, and visualize in tables or charts

---

## File Structure Explained

### Backend (`backend/`)
```
app/
  ├── core/              # Configuration & Security
  ├── db/                # Database operations
  ├── ai/                # Gemini AI integration
  ├── services/          # Business logic
  ├── api/routes/        # REST endpoints
  ├── models/            # Data models
  └── main.py            # FastAPI entry point

tests/                   # Unit tests
requirements.txt        # Python dependencies
Dockerfile              # Docker image
docker-compose.yml      # Service orchestration
```

### Frontend (`frontend/`)
```
src/
  ├── api/               # API client
  ├── components/        # React components (8)
  ├── pages/             # Page components
  ├── store/             # State management
  ├── hooks/             # Custom hooks
  ├── types/             # TypeScript interfaces
  ├── utils/             # Helper functions
  ├── App.tsx            # Root component
  └── main.tsx           # Entry point

package.json            # npm dependencies
vite.config.ts          # Vite configuration
tailwind.config.js      # TailwindCSS config
tsconfig.json           # TypeScript config
```

---

## Key API Endpoints

### Connection
- `POST /api/v1/connect/test` - Test database connection
- `GET /api/v1/connect/status` - Get status

### Schema
- `GET /api/v1/schema/metadata` - Full schema info
- `GET /api/v1/schema/tables` - List tables
- `GET /api/v1/schema/columns` - List columns

### SQL Generation
- `POST /api/v1/generate/sql` - Generate SQL from natural language

### Preview & Execute
- `POST /api/v1/preview/execute` - Preview query
- `POST /api/v1/execute/query` - Execute query

### History
- `GET /api/v1/history/queries` - Get query history
- `DELETE /api/v1/history/clear` - Clear history

See full API docs at http://localhost:8000/docs when backend is running.

---

## UI Components

### Left Side: Schema Viewer
- Browse all tables
- View columns with types
- See relationships
- Search tables

### Center: Chat & Editor
- **Chat Panel**: Type natural language queries
- **Query Editor**: Edit generated SQL
- Switch between both modes

### Right Side: Results
- **Table View**: Paginated results (10 rows per page)
- **Chart View**: Auto-detect and visualize data
- Switch between table and chart

### History Sidebar
- Track all executed queries
- View execution times
- Re-run previous queries
- Clear history

### Mode Selector
- **Safe Mode**: SELECT queries only
- **Edit Mode**: All query types with confirmation

---

## Common Tasks

### Connect to Remote Database
1. Click "Connect"
2. Enter your database credentials
3. Click "Connect" button

### Generate SQL from Natural Language
1. Type your query in the chat panel
2. Click "Generate SQL"
3. AI will create SQL with explanation

### Preview Before Executing
1. Click "Preview" button
2. See affected rows and data
3. Make adjustments if needed

### See Query Results as Chart
1. Click "Chart" tab in results area
2. Select from suggested chart types
3. View visualization

### Clear Query History
1. Click history sidebar
2. Click "Clear History"
3. Confirm when prompted

---

## Troubleshooting

### Connection Issues
**Problem**: Can't connect to database
- Check PostgreSQL is running
- Verify credentials (default: postgres/postgres)
- Check DATABASE_URL environment variable

**Problem**: Backend not found (API calls fail)
- Check backend is running on port 8000
- Check VITE_API_URL in frontend .env
- Check CORS is enabled (should be in FastAPI)

### Port Already in Use
**Problem**: Port 5173 (frontend) or 8000 (backend) already in use

```bash
# On macOS/Linux - find process using port
lsof -i :5173
lsof -i :8000

# Kill process (replace PID with process ID)
kill -9 PID

# Or use different ports in configuration
```

### Api Key Issues
**Problem**: "Invalid API Key" error
- Get key from https://makersuite.google.com/app/apikey
- Make sure it's set as environment variable
- Restart backend after changing key

**Problem**: Gemini API not working
- Check your API key is active
- Check you haven't exceeded quotas
- Check internet connection

### TypeScript Errors in Frontend
```bash
cd frontend
npm run type-check  # Check types
npm run lint        # Check linting
```

---

## Useful Commands

### Frontend
```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
npm run type-check   # Type check TypeScript
npm run lint         # Run linting
```

### Backend
```bash
uvicorn app.main:app --reload           # Start with hot reload
uvicorn app.main:app --reload --port 9000  # Different port
python -m pytest                         # Run tests
python -m pytest -v                      # Verbose output
```

### Docker
```bash
docker-compose up                  # Start all services
docker-compose down                # Stop all services
docker-compose logs -f             # View logs
docker-compose restart             # Restart services
```

---

## Next Steps

1. ✅ Install dependencies on your machine
2. ✅ Set GOOGLE_API_KEY environment variable
3. ✅ Start docker-compose or local development
4. ✅ Try connecting to a database
5. ✅ Generate a SQL query from natural language
6. ✅ Execute it and see results
7. ✅ Explore the API documentation
8. ✅ Customize for your needs

---

## Documentation

- **Full Overview**: See [README.md](README.md)
- **Backend Details**: See [backend/README.md](backend/README.md)
- **Frontend Details**: See [frontend/README.md](frontend/README.md)
- **Deployment Guide**: See [frontend/SETUP.md](frontend/SETUP.md)
- **API Reference**: See [backend/API_REFERENCE.md](backend/API_REFERENCE.md)

---

## Support & Resources

### Getting API Key
Visit: https://makersuite.google.com/app/apikey

### Learn More
- FastAPI Docs: https://fastapi.tiangolo.com
- React Docs: https://react.dev
- PostgreSQL Docs: https://www.postgresql.org/docs
- Docker Docs: https://docs.docker.com

---

**Ready to go!** 🚀

Your complete, production-ready full-stack application is ready to use. Start with Docker Compose for the fastest setup, or follow the local development guide for more control.

Questions? Check the documentation files or examine the source code - everything is well-commented and organized.
