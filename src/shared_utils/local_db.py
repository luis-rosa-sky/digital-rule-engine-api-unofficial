"""Rules local db evaluator module"""

# Third-party library imports
from .db_manager import DatabaseManager

class LocalDatabase:
    """Class responsible for evaluating rules on campaigns stored in a local database."""

    def __init__(self):
        """Initialize the RulesLocalDBEvaluator with database connection."""
        self.db_manager = DatabaseManager()

    def fetch_data(self, table, columns, condition=None):
        """Fetch campaign data from the database."""
        rows = self.db_manager.select(table, columns, condition)
        
        # Convert rows to a list of dictionaries (JSON-like structure)
        return [dict(zip(columns, row)) for row in rows]

    def insert(self, table, id, insert_data):
        """Insert facts into the local database."""
        self.db_manager.insert(table, insert_data, f"id = {id}")

    def update(self, table, id, updated_data):
        """Update a campaign's data in the database."""
        self.db_manager.update(table, updated_data, f"id = {id}")

    def delete(self, table, id):
        """Delete a campaign from the database."""
        self.db_manager.delete(table, f"id = {id}")

    def sync(self, table, facts):
        """Process facts and perform actions such as insert, update, or delete."""
        for fact in facts:
            if fact['action'] == 'sync':
                self.insert(table, fact['data'])
            elif fact['action'] == 'update':
                self.update(table, fact['data']['id'], fact['data'])
            elif fact['action'] == 'delete':
                self.delete(table, fact['data']['id'])