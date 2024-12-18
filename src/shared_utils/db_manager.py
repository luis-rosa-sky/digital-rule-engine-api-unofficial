"""Database manager module"""

# Third-party library imports
from .config import get_config
from psycopg2 import connect, OperationalError, sql

class DatabaseManager:
    def __init__(self):
        """
        Initialize the DatabaseManager with connection parameters.
        """
        """
        Establishes and returns a connection to the database using configuration values.

        Returns:
            psycopg2.extensions.connection: A connection object to the PostgreSQL database.

        Raises:
            ValueError: If required configuration values are missing.
            OperationalError: If there is an error connecting to the database.
        """
        # Load database configuration
        self.config = get_config("database")

        # Ensure all required configuration values are present
        required_keys = ["dbname", "user", "password", "host", "port"]
        if not all(key in self.config for key in required_keys):
            raise ValueError("Missing required database configuration keys.")

        try:
            self.conn = connect(
                dbname=self.config["dbname"],
                user=self.config["user"],
                password=self.config["password"],
                host=self.config["host"],
                port=self.config["port"]
            )
        except OperationalError as e:
            raise OperationalError(f"Error connecting to the database: {e}") from e
    
    def insert(self, table, data):
        """
        Insert a row into a table.
        
        :param table: Table name as a string.
        :param data: Dictionary of column-value pairs.
        """
        columns = data.keys()
        values = tuple(data.values())
        
        query = sql.SQL("""
            INSERT INTO {table} ({columns})
            VALUES ({placeholders})
            ON CONFLICT DO NOTHING
        """).format(
            table=sql.Identifier(table),
            columns=sql.SQL(", ").join(map(sql.Identifier, columns)),
            placeholders=sql.SQL(", ").join(sql.Placeholder() * len(columns))
        )
        
        with self.conn.cursor() as cur:
            cur.execute(query, values)
        self.conn.commit()

    def update(self, table, data, condition):
        """
        Update rows in a table.
        
        :param table: Table name as a string.
        :param data: Dictionary of column-value pairs to update.
        :param condition: Condition for the update as a string (e.g., "id = %s").
        """
        columns = data.keys()
        values = tuple(data.values())
        
        set_clause = sql.SQL(", ").join(
            [sql.SQL("{} = %s").format(sql.Identifier(col)) for col in columns]
        )
        
        query = sql.SQL("""
            UPDATE {table}
            SET {set_clause}
            WHERE {condition}
        """).format(
            table=sql.Identifier(table),
            set_clause=set_clause,
            condition=sql.SQL(condition)
        )
        
        with self.conn.cursor() as cur:
            cur.execute(query, values)
        self.conn.commit()

    def delete(self, table, condition):
        """
        Delete rows from a table.
        
        :param table: Table name as a string.
        :param condition: Condition for the deletion as a string (e.g., "id = %s").
        """
        query = sql.SQL("""
            DELETE FROM {table}
            WHERE {condition}
        """).format(
            table=sql.Identifier(table),
            condition=sql.SQL(condition)
        )
        
        with self.conn.cursor() as cur:
            cur.execute(query)
        self.conn.commit()

    def select(self, table, columns="*", condition=None):
        """
        Select rows from a table.
        
        :param table: Table name as a string.
        :param columns: List of columns to select or "*" for all.
        :param condition: Optional condition as a string (e.g., "id = %s").
        :return: List of rows matching the query.
        """
        columns = sql.SQL(", ").join(map(sql.Identifier, columns)) if columns != "*" else sql.SQL("*")
        query = sql.SQL("SELECT {columns} FROM {table}").format(
            columns=columns,
            table=sql.Identifier(table)
        )
        
        if condition:
            query += sql.SQL(" WHERE {condition}").format(condition=sql.SQL(condition))
        
        with self.conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
        return rows

    def close(self):
        """
        Close the database connection.
        """
        self.conn.close()
