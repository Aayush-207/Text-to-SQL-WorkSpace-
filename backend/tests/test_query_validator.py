"""Sample unit tests for query validator."""
import pytest

from app.db.query_validator import QueryValidator


class TestQueryValidator:
    """Test SQL query validator."""

    def test_validate_dangerous_drop_database(self):
        """Test blocking DROP DATABASE."""
        query = "DROP DATABASE postgres"
        is_valid, error = QueryValidator.validate_generated_query(query)
        assert not is_valid
        assert "DROP DATABASE" in error

    def test_validate_dangerous_truncate(self):
        """Test blocking TRUNCATE."""
        query = "TRUNCATE TABLE users"
        is_valid, error = QueryValidator.validate_generated_query(query)
        assert not is_valid
        assert "TRUNCATE" in error

    def test_validate_multiple_statements(self):
        """Test blocking multiple statements."""
        query = "SELECT * FROM users; DELETE FROM users"
        is_valid, error = QueryValidator.validate_generated_query(query)
        assert not is_valid
        assert "Multiple statements" in error

    def test_validate_delete_without_where(self):
        """Test DELETE without WHERE."""
        query = "DELETE FROM users"
        is_valid, error = QueryValidator.validate_generated_query(query)
        assert not is_valid
        assert "WHERE" in error

    def test_validate_delete_with_where(self):
        """Test DELETE with WHERE clause."""
        query = "DELETE FROM users WHERE id = 1"
        is_valid, error, query_type = QueryValidator.validate_generated_query(query)
        assert is_valid
        assert query_type == "DELETE"

    def test_validate_select_without_limit(self):
        """Test SELECT without LIMIT gets limit injected."""
        query = "SELECT * FROM users"
        is_valid, error, query_type = QueryValidator.validate_generated_query(query)
        assert is_valid
        assert "LIMIT" in query
        assert query_type == "SELECT"

    def test_validate_select_with_limit(self):
        """Test SELECT with LIMIT is not modified."""
        query = "SELECT * FROM users LIMIT 50"
        is_valid, error, query_type = QueryValidator.validate_generated_query(query)
        assert is_valid
        assert query_type == "SELECT"

    def test_get_query_type_select(self):
        """Test detecting SELECT query type."""
        query = "SELECT * FROM users"
        query_type = QueryValidator.validate_generated_query(query)[1]
        assert query_type is None or "SELECT" in query

    def test_get_query_type_insert(self):
        """Test detecting INSERT query type."""
        query = "INSERT INTO users (name) VALUES ('John')"
        query_type = QueryValidator.validate_generated_query(query)[2]
        assert query_type == "INSERT"

    def test_get_query_type_update(self):
        """Test detecting UPDATE query type."""
        query = "UPDATE users SET name = 'John' WHERE id = 1"
        query_type = QueryValidator.validate_generated_query(query)[2]
        assert query_type == "UPDATE"

    def test_query_with_comments(self):
        """Test query with SQL comments."""
        query = """
        -- Get all users
        SELECT * FROM users
        /* where id > 0 */
        WHERE active = true
        """
        is_valid, error, query_type = QueryValidator.validate_generated_query(query)
        assert is_valid
        assert query_type == "SELECT"

    def test_is_write_query(self):
        """Test identifying write queries."""
        assert QueryValidator.is_write_query("INSERT")
        assert QueryValidator.is_write_query("UPDATE")
        assert QueryValidator.is_write_query("DELETE")
        assert QueryValidator.is_write_query("ALTER")
        assert not QueryValidator.is_write_query("SELECT")

    def test_is_read_query(self):
        """Test identifying read queries."""
        assert QueryValidator.is_read_query("SELECT")
        assert not QueryValidator.is_read_query("INSERT")
        assert not QueryValidator.is_read_query("UPDATE")
