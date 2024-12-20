# Standard library imports
import time

# Third-party library imports
from fastapi import APIRouter, Request
from src.shared_utils.utils import get_logger
from src.shared_utils.response_handler import ResponseHandler
from src.shared_utils.local_db import LocalDatabase
from ..utils.rules_runner import RulesRunner
from ..utils.rules_performance_metrics import RulesPerformanceMetrics

# Configure logging
logger = get_logger("rule-engine-api")
response_handler = ResponseHandler()
router = APIRouter()

# Instantiate the RulesPerformanceMetrics class
rules_performance_metrics = RulesPerformanceMetrics()

@router.get("/exec-rule-engine")
async def exec_rule_engine(request: Request):
    """
    Execute rule engine endpoint. Logs a message and returns a success response.
    """
    try:
        # Record execution details
        execution_details = {
            "endpoint": request.url.path,  # Get the endpoint path dynamically
            "request_time": time.time(),
        }
        rules_performance_metrics.record_execution_details(execution_details)

        # Start timing for data fetching
        start_time = rules_performance_metrics.start_timer()
        data = await _fetch_data_from_local_database()
        rules_performance_metrics.stop_timer(start_time, "data_fetch_time")

        # Start timing for rules fetching
        start_time = rules_performance_metrics.start_timer()
        rules = await _fetch_rules_from_local_database()
        rules_performance_metrics.stop_timer(start_time, "rules_fetch_time")

        # Run the rules engine asynchronously
        await _run_rules_engine_async(data, rules)

        # Record CPU and memory usage
        rules_performance_metrics.record_cpu_and_memory_usage()

        # Record system-level metrics
        rules_performance_metrics.record_system_metrics()

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

@router.get("/exec-rule-performance-metrics")
def get_rule_performance_metrics():
    """
    Retrieve performance metrics for the rule engine execution.
    """
    return rules_performance_metrics.get_performance_metrics()

async def _fetch_data_from_local_database():
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

async def _fetch_rules_from_local_database():
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

async def _run_rules_engine_async(data, rules):
    """
    Asynchronous wrapper for running the rules engine.
    """
    try:
        start_time = rules_performance_metrics.start_timer()
        rules_runner = RulesRunner()
        await rules_runner.run(data, rules)
        rules_performance_metrics.stop_timer(start_time, "rules_eval_time")
    except Exception as e:
        logger.error(f"Error running rules engine: {e}")
        raise