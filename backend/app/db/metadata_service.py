"""Database metadata extraction service."""
from typing import Any, Dict, List, Optional
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.logger import logger


class MetadataService:
    """Extract and manage database metadata."""

    @staticmethod
    async def get_schema_metadata(session: AsyncSession, schema: str = "public") -> Dict[str, Any]:
        """
        Get complete schema metadata.

        Args:
            session: Database session
            schema: Schema name

        Returns:
            Dictionary containing tables, columns, and relationships
        """
        try:
            tables = await MetadataService.get_tables(session, schema)
            columns = await MetadataService.get_columns(session, schema)
            constraints = await MetadataService.get_constraints(session, schema)
            foreign_keys = await MetadataService.get_foreign_keys(session, schema)
            indexes = await MetadataService.get_indexes(session, schema)

            return {
                "schema": schema,
                "tables": tables,
                "columns": columns,
                "constraints": constraints,
                "foreign_keys": foreign_keys,
                "indexes": indexes,
            }
        except Exception as e:
            logger.error(f"Failed to get schema metadata: {str(e)}")
            raise

    @staticmethod
    async def get_tables(session: AsyncSession, schema: str = "public") -> List[Dict[str, Any]]:
        """
        Get all tables in schema.

        Args:
            session: Database session
            schema: Schema name

        Returns:
            List of table metadata
        """
        query = text(
            """
            SELECT 
                table_name,
                table_type,
                table_schema,
                (SELECT count(*) FROM information_schema.columns 
                 WHERE table_name = t.table_name AND table_schema = t.table_schema) as column_count
            FROM information_schema.tables t
            WHERE table_schema = :schema AND table_type = 'BASE TABLE'
            ORDER BY table_name
            """
        )

        result = await session.execute(query, {"schema": schema})
        rows = result.fetchall()

        return [
            {
                "name": row[0],
                "type": row[1],
                "schema": row[2],
                "column_count": row[3],
            }
            for row in rows
        ]

    @staticmethod
    async def get_columns(session: AsyncSession, schema: str = "public") -> Dict[str, List[Dict[str, Any]]]:
        """
        Get all columns for tables in schema.

        Args:
            session: Database session
            schema: Schema name

        Returns:
            Dictionary mapping table names to column metadata
        """
        query = text(
            """
            SELECT 
                table_name,
                column_name,
                data_type,
                is_nullable,
                column_default,
                ordinal_position
            FROM information_schema.columns
            WHERE table_schema = :schema
            ORDER BY table_name, ordinal_position
            """
        )

        result = await session.execute(query, {"schema": schema})
        rows = result.fetchall()

        columns: Dict[str, List[Dict[str, Any]]] = {}
        for row in rows:
            table_name = row[0]
            if table_name not in columns:
                columns[table_name] = []

            columns[table_name].append(
                {
                    "name": row[1],
                    "data_type": row[2],
                    "is_nullable": row[3] == "YES",
                    "default": row[4],
                    "position": row[5],
                }
            )

        return columns

    @staticmethod
    async def get_foreign_keys(session: AsyncSession, schema: str = "public") -> List[Dict[str, Any]]:
        """
        Get all foreign key relationships.

        Args:
            session: Database session
            schema: Schema name

        Returns:
            List of foreign key relationships
        """
        query = text(
            """
            SELECT 
                kcu1.table_name,
                kcu1.column_name,
                kcu2.table_name as referenced_table,
                kcu2.column_name as referenced_column,
                rc.constraint_name
            FROM information_schema.referential_constraints as rc
            JOIN information_schema.key_column_usage as kcu1 
                ON rc.constraint_name = kcu1.constraint_name AND kcu1.table_schema = :schema
            JOIN information_schema.key_column_usage as kcu2 
                ON rc.unique_constraint_name = kcu2.constraint_name AND kcu2.table_schema = :schema
            ORDER BY kcu1.table_name, kcu1.column_name
            """
        )

        result = await session.execute(query, {"schema": schema})
        rows = result.fetchall()

        return [
            {
                "table": row[0],
                "column": row[1],
                "referenced_table": row[2],
                "referenced_column": row[3],
                "constraint_name": row[4],
            }
            for row in rows
        ]

    @staticmethod
    async def get_constraints(session: AsyncSession, schema: str = "public") -> Dict[str, List[Dict[str, Any]]]:
        """
        Get all constraints.

        Args:
            session: Database session
            schema: Schema name

        Returns:
            Dictionary mapping table names to constraint metadata
        """
        query = text(
            """
            SELECT 
                table_name,
                constraint_name,
                constraint_type
            FROM information_schema.table_constraints
            WHERE table_schema = :schema
            ORDER BY table_name, constraint_name
            """
        )

        result = await session.execute(query, {"schema": schema})
        rows = result.fetchall()

        constraints: Dict[str, List[Dict[str, Any]]] = {}
        for row in rows:
            table_name = row[0]
            if table_name not in constraints:
                constraints[table_name] = []

            constraints[table_name].append(
                {
                    "name": row[1],
                    "type": row[2],
                }
            )

        return constraints

    @staticmethod
    async def get_indexes(session: AsyncSession, schema: str = "public") -> Dict[str, List[Dict[str, Any]]]:
        """
        Get all indexes.

        Args:
            session: Database session
            schema: Schema name

        Returns:
            Dictionary mapping table names to index metadata
        """
        query = text(
            """
            SELECT 
                t.relname as table_name,
                i.relname as index_name,
                a.amname as index_type,
                ix.indisunique,
                ix.indisprimary
            FROM pg_class t
            JOIN pg_index ix ON t.oid = ix.indrelid
            JOIN pg_class i ON i.oid = ix.indexrelid
            JOIN pg_am a ON a.oid = i.relam
            JOIN pg_namespace n ON n.oid = t.relnamespace
            WHERE n.nspname = :schema
            ORDER BY t.relname, i.relname
            """
        )

        result = await session.execute(query, {"schema": schema})
        rows = result.fetchall()

        indexes: Dict[str, List[Dict[str, Any]]] = {}
        for row in rows:
            table_name = row[0]
            if table_name not in indexes:
                indexes[table_name] = []

            indexes[table_name].append(
                {
                    "name": row[1],
                    "type": row[2],
                    "is_unique": row[3],
                    "is_primary": row[4],
                }
            )

        return indexes

    @staticmethod
    async def get_table_sample_data(
        session: AsyncSession,
        table_name: str,
        schema: str = "public",
        limit: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Get sample data from table.

        Args:
            session: Database session
            table_name: Table name
            schema: Schema name
            limit: Number of rows to fetch

        Returns:
            List of sample rows
        """
        try:
            query = text(f'SELECT * FROM "{schema}"."{table_name}" LIMIT :limit')
            result = await session.execute(query, {"limit": limit})
            rows = result.fetchall()

            # Convert to list of dicts
            return [dict(row._mapping) for row in rows]
        except Exception as e:
            logger.error(f"Failed to get sample data from {table_name}: {str(e)}")
            return []
