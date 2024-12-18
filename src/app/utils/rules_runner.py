"""Durable rules runner module"""

# Standard library imports
import json
import asyncio

# Third-party library imports
from src.shared_utils.utils import get_logger
from durable.lang import ruleset, when_all, when_any, m, post
from functools import reduce
from typing import List, Dict, Any

# Configure logging
logger = get_logger("rules-runner")

class RulesRunner:
    """Class responsible for evaluating rules on campaigns stored in a local database."""

    def __init__(self):
        """Initialize the RulesRunner."""
        pass

    async def run(self, data, rules):
 
        for record in data:

            print("=> " + str(record))
            # Define ruleset for campaigns
            for rule in rules['rules']:
                
                logger.info("Ruleset defined and facts fetched.")
                await self._define_rule(rule)
        
                # Evaluate the rules for campaigns and insert/update local database
                logger.info(f"Starting rules evaluation from data")
                await self._evaluate_rule(rule, record)
 
    async def _define_rule(self, rule: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Define rules and process facts.

        Args:
            rules_config (Dict[str, Any]): Configuration containing rules.

        Returns:
            List[Dict[str, Any]]: Processed facts after applying rules.
        """
        ruleset_name = rule['name']
        condition = rule['condition']
        actions = rule['actions']

        with ruleset(ruleset_name):
            logger.info(f"Building conditions for rule: {ruleset_name}")
            if 'all' in condition:
                @when_all(self._build_dynamic_condition(condition['all']))
                def rule_handler_all(c):
                    logger.info(f"Executing rule: {rule['name']}")
                    # Use asyncio.create_task to run the async function
                    asyncio.create_task(self._execute_actions(c, actions))

            elif 'any' in condition:
                @when_any(self._build_dynamic_condition(condition['any'], is_all=False))
                def rule_handler_any(c):
                    logger.info(f"Executing rule: {rule['name']}")
                    asyncio.create_task(self._execute_actions(c, actions))

    async def _evaluate_rule(self, ruleset_name, record):
        """Evaluate rules for each record and post the result."""
            
        for line_item in record["line_items"]:
            # Find the corresponding campaign by ID
            campaign = next(
                (camp for camp in record["campaigns"] if camp["id"] == line_item["campaign_id"]), {}
            )

            # Combine line item and campaign data into a single record
            record = {
                "line_item" : {
                    "performance" : line_item["performance"],
                    "remaining_inventory" : line_item["remaining_inventory"],
                    "allocated_impressions" : line_item["allocated_impressions"],
                    "status" : line_item["status"],
                    "inventory_level" : line_item["inventory_level"]
                },
                "campaign": {
                    "id": campaign["id"],
                    "priority" : campaign["priority"]
                }
            }
       
        # Ensure the record can be serialized into JSON
        await self._execute_post(ruleset_name, record)

    def _build_dynamic_condition(self, conditions: List[Dict[str, Any]], is_all: bool = True) -> Any:
        """Build dynamic condition expressions.

        Args:
            conditions (List[Dict[str, Any]]): List of conditions to be evaluated.
            is_all (bool): Whether to use 'all' or 'any' logic.

        Returns:
            Any: Combined condition expression.
        """
        expressions = [self._create_expression(cond['field'].split('.'), cond['operator'], cond['value']) for cond in conditions]
        return reduce(lambda x, y: x & y if is_all else x | y, expressions)

    def _create_expression(self, field_path: List[str], operator: str, value: Any) -> Any:
        """Create a condition expression dynamically.

        Args:
            field_path (List[str]): Path to the field in the fact.
            operator (str): Operator to use in the condition.
            value (Any): Value to compare against.

        Returns:
            Any: Constructed condition expression.
        """
        expr = m
        for key in field_path:
            expr = getattr(expr, key)

        if operator == '==':
            return expr == value
        elif operator == '!=':
            return expr != value
        elif operator == '<':
            return expr < value
        elif operator == '>':
            return expr > value
        elif operator == '<=':
            return expr <= value
        elif operator == '>=':
            return expr >= value
        else:
            raise ValueError(f"Unsupported operator: {operator}")

    async def _execute_actions(self, c, actions: List[Dict[str, Any]]) -> None:
        """Execute actions based on the rule.

        Args:
            c: Context object.
            actions (List[Dict[str, Any]]): List of actions to be executed.
        """
        await asyncio.sleep(1)  # Simulate an asynchronous delay
        for action in actions:
            try:
                if action['type'] == 'update':
                    self._perform_update(c, action)
                elif action['type'] == 'redistribute':
                    logger.info(f"Redistributing impressions: {action['params']}")
                elif action['type'] == 'alert':
                    logger.info(f"Alert: {action['message']}")
                elif action['type'] == 'notify':
                    logger.info(f"Notification sent to {action['recipient']}: {action['template']}", c.m.campaign.id)
            except Exception as e:
                logger.error(f"Error executing action {action['type']}: {e}")

    def _perform_update(self, c, action: Dict[str, Any]) -> None:
        """Perform update action.

        Args:
            c: Context object.
            action (Dict[str, Any]): Action configuration.
        """
        try:
            logger.info(f"Updating: {action['target_field']} with expression: {action['expression']}")
            
            # Ensure the context object is not None
            if c.m is None:
                raise ValueError("Context object is None")

            # Evaluate the expression based on the context fact
            try:
                expression_result = eval(action['expression'], {}, c.m)
            except Exception as e:
                logger.error(f"Error evaluating expression {action['expression']}: {e}")
                raise

            keys = action['target_field'].split('.')
            target = c.m

            # Navigate through the target field path in the context
            for key in keys[:-1]:
                if key not in target:
                    target[key] = {}
                target = target[key]

            # Update the final key with the evaluated result
            target[keys[-1]] = expression_result
            logger.info(f"Updated {action['target_field']} to {expression_result}")
        except Exception as e:
            logger.error(f"Error updating field {action['target_field']}: {e}")

    async def _execute_post(self, ruleset_name, message):
        try:
            # Debugging: Check types before calling post
            if callable(ruleset_name):
                raise TypeError("ruleset_name is a function, not a string.")
            if callable(message):
                raise TypeError("record is a function, not a dictionary.")
            
            # Validate JSON serializability
            try:
                json.dumps(message)
            except TypeError as te:
                raise ValueError(f"Record is not JSON serializable: {te}")
                        
            # Call the post function (assuming it's defined elsewhere)
            post(ruleset_name, message)
        except Exception as e:
            logger.error("Error occurred: %s", e, exc_info=True)