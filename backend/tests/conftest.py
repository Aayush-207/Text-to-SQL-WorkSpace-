"""Conftest for pytest setup."""
import pytest
from unittest.mock import AsyncMock


@pytest.fixture
def mock_session():
    """Create mock database session."""
    session = AsyncMock()
    return session


@pytest.fixture
def sample_metadata():
    """Create sample database metadata."""
    return {
        "schema": "public",
        "tables": [
            {"name": "users", "type": "BASE TABLE", "schema": "public", "column_count": 5},
            {"name": "orders", "type": "BASE TABLE", "schema": "public", "column_count": 4},
        ],
        "columns": {
            "users": [
                {"name": "id", "data_type": "integer", "is_nullable": False, "position": 1},
                {"name": "email", "data_type": "character varying", "is_nullable": False, "position": 2},
                {"name": "created_at", "data_type": "timestamp", "is_nullable": False, "position": 5},
            ],
            "orders": [
                {"name": "id", "data_type": "integer", "is_nullable": False, "position": 1},
                {"name": "user_id", "data_type": "integer", "is_nullable": False, "position": 2},
                {"name": "created_at", "data_type": "timestamp", "is_nullable": False, "position": 4},
            ],
        },
        "foreign_keys": [
            {
                "table": "orders",
                "column": "user_id",
                "referenced_table": "users",
                "referenced_column": "id",
                "constraint_name": "fk_orders_users",
            }
        ],
        "constraints": {
            "users": [
                {"name": "pk_users", "type": "PRIMARY KEY"},
                {"name": "uq_users_email", "type": "UNIQUE"},
            ]
        },
        "indexes": {
            "users": [{"name": "idx_users_email", "type": "btree", "is_unique": True, "is_primary": False}]
        },
    }


@pytest.fixture
def sample_query_result():
    """Create sample query result."""
    return [
        {"id": 1, "email": "user1@example.com", "created_at": "2024-01-01"},
        {"id": 2, "email": "user2@example.com", "created_at": "2024-01-02"},
        {"id": 3, "email": "user3@example.com", "created_at": "2024-01-03"},
    ]
