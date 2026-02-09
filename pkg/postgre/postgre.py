import logging
from typing import Any

import psycopg
from psycopg import connect, sql
from psycopg.rows import dict_row

logger = logging.getLogger(__name__)


class PostgreDB:
    def __init__(self, db_url: str):
        """
        Initializes the client with a connection string.
        Example db_url: "postgresql://user:password@localhost:5432/postgres"
        """
        self.db_url = db_url

    def _get_conn(self):
        # row_factory=dict_row allows us to get results as dictionaries
        # e.g., result['chat_id'] instead of result[0]
        return psycopg.connect(self.db_url, row_factory=dict_row)

    def execute_query(self, query, params=None):
        """Executes a query that doesn't return data (INSERT, UPDATE, DELETE)."""
        try:
            with self._get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, params)
                    conn.commit()
        except Exception:
            logger.exception("execute_query error")

    async def execute_many(
        self, query: str, data: list, returning_col: str = None
    ) -> list[Any]:
        results = []
        # 1. Prepare the query
        if returning_col:
            final_query = sql.SQL("{} RETURNING {}").format(
                sql.SQL(query.strip().rstrip(";")), sql.Identifier(returning_col)
            )
        else:
            final_query = sql.SQL(query)

        try:
            with connect(self.db_url) as conn:
                with conn.cursor() as cur:
                    if returning_col:
                        # Case A: We want data back
                        cur.executemany(final_query, data, returning=True)
                        while True:
                            row = cur.fetchone()
                            if row is not None:
                                results.append(row[0])
                            if not cur.nextset():
                                break
                    else:
                        # Case B: Standard bulk insert, no results
                        cur.executemany(final_query, data)

            return results
        except Exception:
            logger.exception("execute_many error")
            return []

    async def fetch_all(self, query, params=None):
        """Executes a query and returns all matching rows."""
        try:
            with self._get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, params)
                    return cur.fetchall()
        except Exception:
            logger.exception("fetch_all error")
            return []

    async def fetch_one(self, query, params=None):
        """Executes a query and returns a single row."""
        try:
            with self._get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, params)
                    return cur.fetchone()
        except Exception as e:
            logger.error(f"fetch_one error: {e}")
            return None
