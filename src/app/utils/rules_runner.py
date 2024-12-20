"""Durable rules runner module using multiprocessing"""

# Standard library imports
import json

# Third-party library imports
from src.shared_utils.utils import get_logger
from durable.lang import ruleset, when_all, when_any, m, post
from functools import reduce
from multiprocessing import Pool
from typing import List, Dict, Any

# Configure logging
logger = get_logger("rules-runner")

class RulesRunner:
    """Class responsible for evaluating rules on campaigns stored in a local database."""

    def __init__(self):
        """Initialize the RulesRunner."""
        pass

    def run(self, data: List[Dict[str, Any]], rules: List[Dict[str, Any]]):
        """
        Run the rules evaluation process using multiprocessing.

        Args:
            data: List of records to evaluate.
            rules: List of rules to apply.
        """
        # Create a pool of worker processes
        with Pool() as pool:
            # Map the rules evaluation to the worker processes
            pool.starmap(self._process_rule, [(rule, data) for rule in rules])

    def _process_rule(self, rule: Dict[str, Any], data: List[Dict[str, Any]]):
        """
        Process a single rule and evaluate it against the data.

        Args:
            rule: The rule to process.
            data: The data to evaluate the rule against.
        """
        rule_data = rule['rule']
        
        logger.info("Ruleset defined and facts fetched.")
        self._define_rule(rule_data)

        logger.info(f"Starting rules evaluation for rule: {rule_data['name']}")
        self._evaluate_rule(rule_data, data)

    def _define_rule(self, rule: Dict[str, Any]):
        """
        Define a rule and process facts.

        Args:
            rule: The rule to define.
        """
        ruleset_name = rule['name']
        condition = rule['condition']
        actions = rule['actions']

        logger.info(f"Defining Rule ({ruleset_name}, {condition}) => {actions}")

        with ruleset(ruleset_name):
            logger.info(f"Building conditions for rule: {ruleset_name}")

            # Handle 'all' conditions
            if 'all' in condition:
                @when_all(self._build_dynamic_condition(condition['all']))
                def rule_handler_all(c):
                    logger.info(f"Executing rule: {ruleset_name}")
                    self._execute_actions(c, actions)

            # Handle 'any' conditions
            elif 'any' in condition:
                @when_any(self._build_dynamic_condition(condition['any'], is_all=False))
                def rule_handler_any(c):
                    logger.info(f"Executing rule: {ruleset_name}")
                    self._execute_actions(c, actions)

            # Default rule: Handle any message that doesn't match other rules
            @when_all(+m.campaign_id)
            def default_handler(c):
                logger.info(f"Default rule matched: Campaign {c.m.campaign_id} does not match any specific rules.")

    def _evaluate_rule(self, rule: Dict[str, Any], data: List[Dict[str, Any]]):
        """
        Evaluate rules for each record and post the result.

        Args:
            rule: The rule to evaluate.
            data: The data to evaluate the rule against.
        """
        ruleset_name = rule['name']
        for record in data:
            logger.info(f"Evaluating Rule ({ruleset_name}) => {record}")

            # Post the record for evaluation
            self._execute_post(ruleset_name, record)

    def _build_dynamic_condition(self, conditions: List[Dict[str, Any]], is_all: bool = True) -> Any:
        """
        Build dynamic condition expressions.

        Args:
            conditions: List of conditions to be evaluated.
            is_all: Whether to use 'all' or 'any' logic.

        Returns:
            Combined condition expression.
        """
        expressions = [self._create_expression(cond['field'].split('.'), cond['operator'], cond['value']) for cond in conditions]
        return reduce(lambda x, y: x & y if is_all else x | y, expressions)

    def _create_expression(self, field_path: List[str], operator: str, value: Any) -> Any:
        """
        Create a condition expression dynamically.

        Args:
            field_path: Path to the field in the fact.
            operator: Operator to use in the condition.
            value: Value to compare against.

        Returns:
            Constructed condition expression.
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

    def _execute_actions(self, c, actions: List[Dict[str, Any]]) -> None:
        """
        Execute actions based on the rule.

        Args:
            c: Context object.
            actions: List of actions to be executed.
        """
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
        """
        Perform update action.

        Args:
            c: Context object.
            action: Action configuration.
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

    def _execute_post(self, ruleset_name: str, record: Dict[str, Any]):
        """
        Post the record for evaluation.

        Args:
            ruleset_name: Name of the ruleset.
            record: The record to post.
        """
        try:
            # Validate JSON serializability
            json.dumps(record)

            post(ruleset_name, record)
        except Exception as e:
            logger.error(f"Error posting record to ruleset {ruleset_name}: {e}")