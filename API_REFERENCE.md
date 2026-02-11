"""Quick reference for API endpoints."""
# Text to SQL API Quick Reference

## Base URL
http://localhost:8000

## Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- API Info: http://localhost:8000/

## Health & Status

### Check API Health
```
GET /health
```

### Get API Information
```
GET /
```

---

## Database Connection

### Test Database Connection
```
POST /api/v1/connect/test
Content-Type: application/json

{
  "host": "localhost",
  "port": 5432,
  "database": "postgres",
  "user": "postgres",
  "password": "password"
}
```

### Get Connection Status
```
GET /api/v1/connect/status
```

---

## Database Schema

### Get Complete Schema Metadata
```
GET /api/v1/schema/metadata?schema=public
```

### List All Tables
```
GET /api/v1/schema/tables?schema=public
```

### Get Column Information
```
GET /api/v1/schema/columns?schema=public
```

### Get Foreign Key Relationships
```
GET /api/v1/schema/foreign-keys?schema=public
```

### Get Database Indexes
```
GET /api/v1/schema/indexes?schema=public
```

### Get Sample Data from Table
```
GET /api/v1/schema/sample-data?table=users&schema=public&limit=5
```

---

## SQL Generation

### Generate SQL from Natural Language
```
POST /api/v1/generate/sql
Content-Type: application/json

{
  "natural_language_query": "Get all users from California",
  "schema": "public"
}

Response:
{
  "success": true,
  "sql": "SELECT * FROM users WHERE state = 'CA' LIMIT 100",
  "type": "SELECT",
  "confidence": 0.95,
  "explanation": "Fetches users from California..."
}
```

### Get Available Models
```
GET /api/v1/generate/available-models
```

---

## Query Preview

### Preview Query Execution
```
POST /api/v1/preview/execute
Content-Type: application/json

{
  "sql": "DELETE FROM logs WHERE date < '2024-01-01'",
  "limit": 100
}

Response:
{
  "success": true,
  "query_type": "DELETE",
  "affected_rows": 500,
  "preview_rows": [...]
}
```

### Simulate Query Execution
```
POST /api/v1/preview/simulate
Content-Type: application/json

{
  "sql": "UPDATE users SET status = 'inactive' WHERE last_login < '2024-01-01'",
  "limit": 100
}
```

---

## Query Execution

### Execute Query
```
POST /api/v1/execute/query
Content-Type: application/json

{
  "sql": "SELECT * FROM users WHERE id = 1"
}

Response:
{
  "success": true,
  "query_type": "SELECT",
  "rows_returned": 1,
  "data": [{"id": 1, "email": "..."}]
}
```

### Execute Multiple Queries
```
POST /api/v1/execute/batch
Content-Type: application/json

[
  {"sql": "SELECT COUNT(*) FROM users"},
  {"sql": "SELECT COUNT(*) FROM orders"}
]
```

### Explain Query Metadata
```
POST /api/v1/execute/explain
Content-Type: application/json

{
  "sql": "SELECT users.*, COUNT(orders.id) FROM users LEFT JOIN orders ON users.id = orders.user_id GROUP BY users.id"
}

Response:
{
  "success": true,
  "query": "SELECT ...",
  "metadata": {
    "tables": ["users", "orders"],
    "columns": ["*", "COUNT(orders.id)"],
    "joins": [{"table": "orders", "condition": "users.id = orders.user_id"}],
    "where_conditions": []
  }
}
```

---

## Query History

### Get Query History
```
GET /api/v1/history/queries?limit=50&query_type=SELECT&success_only=false
```

### Get History Statistics
```
GET /api/v1/history/statistics
```

### Clear Query History
```
DELETE /api/v1/history/clear
```

---

## Common Curl Examples

### Generate and Execute SQL in One Flow
```bash
# 1. Get schema
curl http://localhost:8000/api/v1/schema/metadata

# 2. Generate SQL
curl -X POST http://localhost:8000/api/v1/generate/sql \
  -H "Content-Type: application/json" \
  -d '{"natural_language_query": "Get users", "schema": "public"}'

# 3. Preview (if DELETE/UPDATE)
curl -X POST http://localhost:8000/api/v1/preview/execute \
  -H "Content-Type: application/json" \
  -d '{"sql": "DELETE FROM users WHERE inactive = true"}'

# 4. Execute
curl -X POST http://localhost:8000/api/v1/execute/query \
  -H "Content-Type: application/json" \
  -d '{"sql": "SELECT * FROM users LIMIT 10"}'
```

---

## Error Responses

All errors return:
```json
{
  "success": false,
  "error": "Error message",
  "detail": "Additional details (if debug=true)"
}
```

---

## Response Codes

- `200`: Success
- `400`: Bad Request
- `500`: Server Error
- `503`: Service Unavailable

---

## Tips

1. Always check `/health` before making requests
2. Use `/api/v1/schema/metadata` to understand database structure
3. Preview DELETE/UPDATE queries before execution
4. Check `/docs` for interactive API testing
5. Use `limit` parameter in preview requests
