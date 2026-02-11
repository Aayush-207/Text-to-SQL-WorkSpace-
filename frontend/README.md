# Text to SQL - Frontend

Modern React + TypeScript + Vite frontend for the Text to SQL AI-powered database query tool.

## Features

✨ **Modern Tech Stack**
- React 18+ with TypeScript
- Vite for blazing-fast development
- TailwindCSS for utility-first styling
- Axios for HTTP requests
- Recharts for data visualization

🎨 **Components**
- DatabaseConnector - Connect to PostgreSQL databases
- SchemaViewer - Browse database schema
- ChatPanel - Natural language query input
- QueryEditor - SQL editor with syntax highlighting
- ResultTable - Paginated result display
- ChartViewer - Auto-detect and visualize data
- ConfirmationModal - Safe query execution
- QueryHistory - Query tracking

🚀 **Features**
- AI-powered natural language to SQL conversion
- Safe Mode (SELECT only) and Edit Mode (all queries)
- Query preview before execution
- Automatic chart type detection
- Query history with timestamps
- Real-time database schema browsing

## Getting Started

### Prerequisites
- Node.js 16+
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

### Environment Configuration

Create a `.env` file:

```env
VITE_API_URL=http://localhost:8000
```

## Project Structure

```
src/
├── api/                 # API client and endpoints
│   ├── client.ts       # Axios instance
│   └── endpoints.ts    # All API endpoints
├── components/         # React components
│   ├── DatabaseConnector.tsx
│   ├── SchemaViewer.tsx
│   ├── ChatPanel.tsx
│   ├── QueryEditor.tsx
│   ├── ResultTable.tsx
│   ├── ChartViewer.tsx
│   ├── ConfirmationModal.tsx
│   └── QueryHistory.tsx
├── pages/              # Page components
│   └── Dashboard.tsx
├── store/              # State management
│   └── DatabaseContext.tsx
├── hooks/              # Custom React hooks
│   └── useDatabase.ts
├── types/              # TypeScript type definitions
│   └── index.ts
├── utils/              # Utility functions
│   └── helpers.ts
├── App.tsx             # Root component
├── main.tsx            # Entry point
└── index.css           # Global styles
```

## Component Documentation

### DatabaseConnector
Connection form for PostgreSQL databases.

```tsx
<DatabaseConnector onConnected={() => {}} />
```

### SchemaViewer
Displays database schema with collapsible tables.

```tsx
<SchemaViewer schema={schema} onTableSelect={(table) => {}} />
```

### ChatPanel
Natural language query input with suggestions.

```tsx
<ChatPanel onSQLGenerated={(sql) => {}} />
```

### QueryEditor
SQL editor with line numbers and syntax support.

```tsx
<QueryEditor
  sql={currentSQL}
  onChange={setSQL}
  queryType="SELECT"
  onExecute={handleExecute}
/>
```

### ResultTable
Paginated results display with AUTO-handling.

```tsx
<ResultTable data={results} rowsAffected={10} />
```

### ChartViewer
Auto-detects chart types and visualizes data.

```tsx
<ChartViewer data={results} selectedChart={chart} />
```

## Hooks

### useDatabase
Main hook for database operations.

```tsx
const {
  state,
  connectDatabase,
  generateSQL,
  previewQuery,
  executeQuery,
  getQueryHistory,
} = useDatabase();
```

## API Integration

All API calls go through the context-based state management:

```tsx
// Generate SQL from natural language
const sql = await generateSQL('Show me all users', 'public');

// Preview query without execution
const preview = await previewQuery(sql);

// Execute query
const results = await executeQuery(sql);
```

## Styling

Uses TailwindCSS utility classes. Customize in `tailwind.config.js`.

### Custom Colors
- Primary Blue: `bg-blue-600`
- Success Green: `bg-green-600`
- Warning Yellow: `bg-yellow-100`
- Error Red: `bg-red-600`

## Performance

- Code splitting enabled
- Tree-shaking for unused code
- Minification in production
- Responsive lazy loading

## Development

```bash
# Type checking
npm run type-check

# Linting
npm run lint

# Preview production build
npm run preview
```

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

Created as part of Text to SQL project.
