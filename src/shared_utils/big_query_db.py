"""Rules big query evaluator module"""

# Third-party library imports
from google.cloud import bigquery
from google.oauth2 import service_account

class BigQueryDatabase:
    """Class responsible for evaluating rules on campaigns stored in a cloud database."""

    def __init__(self):
        """Initialize the RulesBigQueryEvaluator with database connection."""
        # Create credentials from the service account key file
        self.credentials = service_account.Credentials.from_service_account_file(
            "config/service_account_key.json",
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )
 
        # Initialize the BigQuery client with the credentials
        self.client = bigquery.Client(credentials=self.credentials, 
                                      project=self.credentials.project_id)

    def fetch_data(self, query):
        """Fetch campaign data from the database."""
        query_job = self.client.query(query)
        results = query_job.result()
        return [dict(row) for row in results]
