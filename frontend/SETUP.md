# Complete Frontend Setup and Deployment Guide

## Quick Start

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Update API URL if different from default
# VITE_API_URL=http://localhost:8000
```

### 3. Development Server
```bash
npm run dev
```
Application opens at http://localhost:5173

### 4. Production Build
```bash
npm run build
npm run preview
```

---

## API Integration

The frontend connects to the backend FastAPI server:

### Default Connection
- **API URL**: `http://localhost:8000`
- **Base Path**: `/api/v1`

### Configure API URL
Edit `.env`:
```env
VITE_API_URL=http://your-backend-url:port
```

### Available Endpoints

**Connection**
- `POST /api/v1/connect/test` - Test database connection
- `GET /api/v1/connect/status` - Get connection status

**Schema**
- `GET /api/v1/schema/metadata` - Get full schema metadata
- `GET /api/v1/schema/tables` - List tables
- `GET /api/v1/schema/columns` - List columns
- `GET /api/v1/schema/foreign-keys` - List foreign keys

**Generation**
- `POST /api/v1/generate/sql` - Generate SQL from natural language

**Preview**
- `POST /api/v1/preview/execute` - Preview query results

**Execution**
- `POST /api/v1/execute/query` - Execute query

**History**
- `GET /api/v1/history/queries` - Get query history
- `DELETE /api/v1/history/clear` - Clear history

---

## Project Structure

```
frontend/
├── src/
│   ├── api/                    # API layer
│   │   ├── client.ts          # Axios instance
│   │   └── endpoints.ts       # All endpoint definitions
│   ├── components/             # React components (8 total)
│   │   ├── DatabaseConnector.tsx
│   │   ├── SchemaViewer.tsx
│   │   ├── ChatPanel.tsx
│   │   ├── QueryEditor.tsx
│   │   ├── ResultTable.tsx
│   │   ├── ChartViewer.tsx
│   │   ├── ConfirmationModal.tsx
│   │   └── QueryHistory.tsx
│   ├── pages/                  # Page-level components
│   │   └── Dashboard.tsx       # Main layout
│   ├── store/                  # State management
│   │   └── DatabaseContext.tsx # Context and reducer
│   ├── hooks/                  # Custom hooks
│   │   └── useDatabase.ts      # Database context hook
│   ├── types/                  # TypeScript definitions
│   │   └── index.ts           # Type definitions
│   ├── utils/                  # Utility functions
│   │   └── helpers.ts         # Data manipulation
│   ├── App.tsx                # Root component
│   ├── main.tsx               # Entry point
│   └── index.css              # Global styles
├── public/                     # Static assets
├── index.html                  # HTML entry
├── package.json                # Dependencies
├── vite.config.ts              # Vite configuration
├── tsconfig.json               # TypeScript config
├── tailwind.config.js          # TailwindCSS config
└── .env                        # Environment variables
```

---

## Component Architecture

### State Management (DatabaseContext)
Central state management for all database operations:

```typescript
interface AppState {
  connected: boolean;
  schema?: SchemaMetadata;
  currentQuery?: string;
  queryHistory: QueryHistoryEntry[];
  mode: 'safe' | 'edit';
  loading: LoadingState;
  error: ErrorState;
  dialog: DialogState;
}
```

### Component Hierarchy

```
App
├── DatabaseProvider
│   └── Dashboard
│       ├── Header
│       ├── Layout (3 columns)
│       │   ├── SchemaViewer (left)
│       │   ├── ChatPanel/QueryEditor (center)
│       │   ├── ResultTable/ChartViewer (right)
│       │   └── QueryHistory (far right)
│       └── ConfirmationModal
```

---

## Features

### 1. Database Connection
- Secure PostgreSQL connection form
- Connection testing before execution
- Password visibility toggle
- Error handling and validation

### 2. Schema Discovery
- Tree-view of all tables
- Column details (type, nullable)
- Foreign key relationships
- Real-time schema search

### 3. Natural Language Processing
- AI-powered SQL generation via Gemini
- Confidence scoring
- Explanation of generated queries
- Query suggestions

### 4. Query Execution
- **Safe Mode**: SELECT queries only
- **Edit Mode**: All query types
- Query preview before execution
- Transaction-safe execution
- Automatic history tracking

### 5. Results Visualization
- Paginated table results
- Automatic chart type detection
- Multiple chart types (bar, line, pie, histogram)
- Data export (future)

### 6. Query History
- Complete query history with timestamps
- Execution statistics
- Success/failure tracking
- Quick re-execution from history

---

## Usage Guide

### Connect to Database
1. Launch application (http://localhost:5173)
2. Enter database credentials:
   - Host: localhost
   - Port: 5432
   - Database: your_database
   - User: your_user
   - Password: your_password
3. Click "Connect"

### Generate Query from Natural Language
1. Select mode (Safe or Edit)
2. Enter natural language query
3. AI generates SQL and explains it
4. For SELECT: executes immediately
5. For writes: shows preview, requires confirmation

### Manual SQL Entry
1. Use the Query Editor panel
2. Write or paste SQL
3. Click "Preview" to review results
4. Click "Execute" to run query
5. View results in table or chart format

### Browse Results
- Switch between Table and Chart views
- Paginate through large result sets
- Auto-detect suitable chart types
- View execution statistics

### Query History
- Left sidebar tracks all queries
- Click to re-run previous queries
- See execution time and status
- Clear history when needed

---

## Development

### Type Checking
```bash
npm run type-check
```

### Linting
```bash
npm run lint
```

### Build for Production
```bash
npm run build
```

---

## Environment Variables

### Required
- `VITE_API_URL`: Backend API base URL (default: http://localhost:8000)

### Optional
- `VITE_APP_NAME`: Application name (default: Text to SQL)
- `VITE_APP_VERSION`: App version (default: 0.1.0)

---

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

---

## Performance Optimization

- Code splitting by route
- Lazy component loading
- Tree-shaking unused imports
- Minified production build
- CSS purging

---

## Troubleshooting

### API Connection Issues
1. Check `VITE_API_URL` in `.env`
2. Ensure backend is running on correct port
3. Check CORS configuration in backend
4. Verify network connectivity

### TypeScript Errors
```bash
npm run type-check
# Fix errors in your IDE or use:
# npm install @types/[package-name]
```

### Build Failures
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Rebuild
npm run build
```

### Port Already in Use
```bash
# Use different port (edit vite.config.ts):
# server: { port: 5174 }
```

---

## Deployment

### Docker
```dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:18-alpine
WORKDIR /app
RUN npm install -g serve
COPY --from=builder /app/dist ./dist
CMD ["serve", "-s", "dist", "-l", "5173"]
```

### Vercel
```bash
npm install -g vercel
vercel
```

### Docker Compose (with Backend)
See backend README for complete setup.

---

## Support

For issues or questions, refer to:
- Backend README (API documentation)
- Component documentation in code
- Issue tracker in repository
