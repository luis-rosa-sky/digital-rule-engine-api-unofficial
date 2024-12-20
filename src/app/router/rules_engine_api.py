# Third-party library imports
# pylint: disable=import-error,broad-exception-caught
from multiprocessing import Process
from fastapi import APIRouter
from src.shared_utils.utils import get_logger
from src.shared_utils.response_handler import ResponseHandler
from src.shared_utils.local_db import LocalDatabase
from ..utils.rules_runner import RulesRunner

# Configure logging
logger = get_logger("rule-engine-api")
response_handler = ResponseHandler()
router = APIRouter()

@router.get("/exc-rule-engine")
def exec_rule_engine():
    """
    Execute rule engine endpoint. Logs a message and returns a success response.
    """
    try:
        # Fetch data and rules synchronously
        data = _fetch_data_from_local_database()
        rules = _fetch_rules_from_local_database()

        # Run the rules engine in a separate process
        process = Process(target=_run_rules_engine_sync, args=(data, rules))
        process.start()
        process.join()

        message = "Rules evaluation completed successfully."
        logger.info(message)
        return message

    except ConnectionError as e:
        message = f"Database connection error: {e}"
        logger.error(message)
        return message
    except KeyError as e:
        message = f"Configuration or key error: {e}"
        logger.error(message)
        return message
    except Exception as e:
        message = f"An unexpected error occurred: {e}"
        logger.error(message)
        return message
    finally:
        message = "Rules evaluation process finished, whether successful or not."
        logger.info(message)
        return response_handler.success(message=message)

def _fetch_data_from_local_database():
    """
    Fetch campaign and line item data from the local database.
    """
    try:
        local_database = LocalDatabase()
        campaigns = local_database.fetch_data('campaign', 
                                            ['id', 'name', 'type', 'start_date', 'end_date'])
        
        data = []
        for campaign in campaigns:
            condition = 'campaign_id=' + str(campaign['id'])
            line_items = local_database.fetch_data('line_item', 
                                                ['id', 'order_id', 'type', 'impressions_delivered', 'impression_goal', 'priority_level', 'delivery_type', 'pacing_osi'],
                                                condition)
            
            # Combine campaign data with line_items data
            for line_item in line_items:
                line_item['pacing_osi'] = float(line_item['pacing_osi'])
                combined_data = {
                    'campaign_id': campaign['id'],
                    'campaign_name': campaign.get('name', ''),  # Example: include campaign name if available
                    **line_item  # Merge line_item fields into the dictionary
                }
                data.append(combined_data)
        
        return data
    except Exception as e:
        logger.error(f"Error fetching data from local database: {e}")
        raise

def _fetch_rules_from_local_database():
    """
    Fetch rule definitions from the local database.
    """
    try:
        local_database = LocalDatabase()
        rules = local_database.fetch_data('rule_definitions', ['id', 'type', 'rule'])
        return rules
    except Exception as e:
        logger.error(f"Error fetching rules from local database: {e}")
        raise

# Synchronous wrapper for the rules engine
def _run_rules_engine_sync(data, rules):
    """
    Synchronous wrapper for running the rules engine in a separate process.
    """
    try:
        rules_runner = RulesRunner()
        rules_runner.run(data, rules)
    except Exception as e:
        logger.error(f"Error running rules engine: {e}")
        raise