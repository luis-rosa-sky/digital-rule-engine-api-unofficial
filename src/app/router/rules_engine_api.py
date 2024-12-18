"""Runner engine api module"""

# Third-party library imports
# pylint: disable=import-error,broad-exception-caught
from fastapi import APIRouter, Depends
from src.shared_utils.utils import get_logger
from src.shared_utils.response_handler import ResponseHandler
from src.shared_utils.decorator_handler import verify_token
from src.shared_utils.local_db import LocalDatabase
from src.shared_utils.big_query_db import BigQueryDatabase
from ..utils.rules_runner import RulesRunner
from ..model.campaign import Campaign
from ..model.line_item import LineItem
 
# Configure logging
logger = get_logger("rule-engine-api")
response_handler = ResponseHandler()
router = APIRouter()

@router.get("/", dependencies=[Depends(verify_token)])
async def exec_rule_engine():
    """
    Execute rule engine endpoint. Logs a message and returns a success response.
    """
    try:
        # Sync between cloud database and local database
        await _sync_cloud_database_to_local_database()

        # Fetch data from the local database
        data = await _fetch_data_from_local_database()

        # Fetch rules from the local database
        rules = await _fetch_rules_from_local_database()

        # Run the rules engine
        await _run_rules_engine(data, rules)

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

async def _sync_cloud_database_to_local_database():
    """
    Fetch campaign and line item data from the BigQuery database.
    """
    try:
        big_query_database = BigQueryDatabase()
        local_database = LocalDatabase()
        campaigns = big_query_database.fetch_data('campaign', 
                                            ['id', 'name', 'type', 'start_date', 'end_date'])
        
        for campaign in campaigns:
            condition = 'campaign_id=' + str(campaign['id'])
            line_items = big_query_database.fetch_data('line_item', 
                                                ['id', 'order_id', 'type', 'impressions_delivered', 'impression_goal', 'priority_level', 'delivery_type', 'pacing_osi'],
                                                condition)
            
            # Add a new campaign in local database
            campaign_obj = Campaign(
                name = campaign['name'],
                type = campaign['type'],
                start_date = campaign['start_date'],
                end_date = campaign['end_date'],
                advertiser = campaign['advertiser'],
                impressions_delivered = campaign['impressions_delivered']
            )
            local_database.insert('campaign', campaign_obj)

            # Add a new line_item in local database
            for line_item in line_items:
                line_item_obj = LineItem(
                    order_id = line_item['order_id'],
                    name = line_item['name'],
                    status = line_item['status'],
                    type = line_item['type'],
                    skippable_ad = line_item['skippable_ad'],
                    impressions_delivered = line_item['impressions_delivered'],
                    impression_goal = line_item['impression_goal'],
                    start_date = line_item['start_date'],
                    end_date = line_item['end_date'],
                    priority_level = line_item['priority_level'],
                    delivery_type = line_item['delivery_type'],
                    bookies = line_item['bookies'],
                    cpm = line_item['cpm'],
                    pacing_osi = line_item['pacing_osi'],
                    targetting_attributes = line_item['targetting_attributes'],
                    creative_dimensions = line_item['creative_dimensions'],
                    vast_error_codes = line_item['vast_error_codes'],
                    ad_unit_mapping = line_item['ad_unit_mapping'],
                    assets_assigned = line_item['assets_assigned'],
                    platform = line_item['platform'],
                    fill_rate = line_item['fill_rate'],
                    campaign_id = line_item['campaign_id']
                )
                local_database.insert('line_item', line_item_obj)
        
    except Exception as e:
        logger.error(f"Error fetching data from BigQuery database: {e}")
        raise

async def _fetch_data_from_local_database():
    """
    Fetch campaign and line item data from the BigQuery database.
    """
    try:
        big_query_database = LocalDatabase()
        campaigns = big_query_database.fetch_data('campaign', 
                                            ['id', 'name', 'type', 'start_date', 'end_date'])
        
        data = []
        for campaign in campaigns:
            condition = 'campaign_id=' + str(campaign['id'])
            line_items = big_query_database.fetch_data('line_item', 
                                                ['id', 'order_id', 'type', 'impressions_delivered', 'impression_goal', 'priority_level', 'delivery_type', 'pacing_osi'],
                                                condition)
            
            # Combine campaign data with line_items data
            for line_item in line_items:
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

async def _run_rules_engine(data, rules):
    """
    Initialize and run the RulesRunner with the provided data and rules.
    """
    try:
        rules_runner = RulesRunner()
        await rules_runner.run(data, rules)
    except Exception as e:
        logger.error(f"Error running rules engine: {e}")
        raise