"""Prompt builder for Gemini AI."""
from typing import Any, Dict, List
from jinja2 import Template


class PromptBuilder:
    """Build prompts for SQL generation."""

    @staticmethod
    def build_sql_generation_prompt(
        user_query: str,
        schema_metadata: Dict[str, Any],
        conversation_history: List[Dict[str, str]] = None,
    ) -> str:
        """
        Build prompt for SQL generation.

        Args:
            user_query: Natural language query from user
            schema_metadata: Database schema metadata
            conversation_history: Previous queries in conversation

        Returns:
            Formatted prompt string
        """
        template_str = """You are an expert SQL database assistant. Your task is to convert natural language questions into SQL queries.

**Database Schema:**
{% for table in tables %}
Table: {{ table.name }}
Columns:
{% for column in columns[table.name] %}
  - {{ column.name }} ({{ column.data_type }}, nullable: {{ column.is_nullable }})
{% endfor %}
{% if foreign_keys[table.name] %}
Foreign Keys:
{% for fk in foreign_keys[table.name] %}
  - {{ fk.column }} references {{ fk.referenced_table }}.{{ fk.referenced_column }}
{% endfor %}
{% endif %}

{% endfor %}

**User Query:** {{ user_query }}

**Requirements:**
1. Generate ONLY valid PostgreSQL syntax
2. Return ONLY a JSON object, no additional text
3. Always include WHERE clauses for safe queries
4. Use appropriate JOINs for related tables
5. Include LIMIT clause for SELECT queries (max 100 rows)
6. Never use DROP, TRUNCATE, or multiple statements
7. Be confident in your response (confidence 0.95 if very sure, 0.7 if less sure)

**Response Format (MUST be valid JSON):**
{
  "sql": "SELECT ... FROM ... WHERE ...",
  "type": "SELECT | INSERT | UPDATE | DELETE | ALTER",
  "confidence": 0.95,
  "explanation": "Brief explanation of what the query does"
}

Generate the SQL query:"""

        template = Template(template_str)

        # Build tables list from schema
        tables = schema_metadata.get("tables", [])
        columns = schema_metadata.get("columns", {})
        foreign_keys_raw = schema_metadata.get("foreign_keys", [])

        # Convert foreign keys to dict for easier lookup
        foreign_keys: Dict[str, List] = {}
        for fk in foreign_keys_raw:
            table = fk["table"]
            if table not in foreign_keys:
                foreign_keys[table] = []
            foreign_keys[table].append(fk)

        prompt = template.render(
            user_query=user_query,
            tables=tables,
            columns=columns,
            foreign_keys=foreign_keys,
        )

        return prompt

    @staticmethod
    def build_sql_explanation_prompt(sql_query: str) -> str:
        """
        Build prompt for SQL explanation.

        Args:
            sql_query: SQL query to explain

        Returns:
            Formatted prompt string
        """
        prompt = f"""Explain the following SQL query in simple terms:

SQL Query:
```sql
{sql_query}
```

Provide:
1. What the query does
2. Key clauses and their purpose
3. Expected output

Keep explanation concise and clear."""

        return prompt

    @staticmethod
    def build_sql_optimization_prompt(
        sql_query: str,
        schema_metadata: Dict[str, Any],
    ) -> str:
        """
        Build prompt for SQL optimization suggestions.

        Args:
            sql_query: SQL query to optimize
            schema_metadata: Database schema metadata

        Returns:
            Formatted prompt string
        """
        prompt = f"""Review this SQL query for optimization opportunities:

SQL Query:
```sql
{sql_query}
```

Database Schema (indexes, constraints):
{str(schema_metadata)}

Provide:
1. Performance issues
2. Suggested optimizations
3. Alternative query approaches

Response format:
{{
  "issues": ["issue1", "issue2"],
  "optimizations": ["opt1", "opt2"],
  "suggested_query": "optimized SQL here"
}}"""

        return prompt
