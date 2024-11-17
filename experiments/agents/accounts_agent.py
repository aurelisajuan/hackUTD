# agents/accounts_agent.py

from .base_agent import BaseAgent
from typing import Any, Dict
from utils.helpers import validate_account_id, get_db, set_db
from swarm.types import Result
import logging
from typing import Callable

# Define the accounts instructions
accounts_instructions = """
You are the Accounts Agent, a highly knowledgeable and professional virtual banking assistant.

Your responsibilities include:
1. Assisting users with account-related requests, such as checking account balances and retrieving bank statements.
2. Answering questions about account features, services, and policies.
3. Ensuring compliance with financial regulations and maintaining customer privacy.
4. Communicating in a polite, empathetic, and user-friendly manner.
"""

class AccountsAgent(BaseAgent):
    def __init__(
        self,
        transfer_to_payments: Callable,
        handle_account_balance: Callable,
        retrieve_bank_statement: Callable
    ):
        super().__init__(
            name="Accounts Agent",
            instructions=accounts_instructions,
            functions=[transfer_to_payments, handle_account_balance, retrieve_bank_statement]
        )

# Define specific functions for Accounts Agent

def handle_account_balance(context_variables: Dict, account_id: str) -> Result:
    logging.info(f"Handling account balance for account ID: {account_id}")
    if not validate_account_id(account_id):
        return Result(
            value="Invalid account ID provided.",
            agent=None  # Transfer back to triage in AgentSwarm
        )
    
    current_db = get_db()
    balance = current_db["accounts"][account_id]["balance"]
    return Result(
        value=f"Your current account balance for {account_id} is ${balance:.2f}.",
        agent=None  # Transfer back to triage in AgentSwarm
    )

def retrieve_bank_statement(context_variables: Dict, account_id: str, period: str) -> Result:
    logging.info(f"Retrieving bank statement for account ID: {account_id}, period: {period}")
    if not validate_account_id(account_id):
        return Result(
            value="Invalid account ID provided.",
            agent=None  # Transfer back to triage in AgentSwarm
        )
    
    current_db = get_db()
    
    # Validate period
    if period not in current_db["accounts"][account_id]["statements"]:
        return Result(
            value=f"No statements found for the period: {period}.",
            agent=None  # Transfer back to triage in AgentSwarm
        )
    
    statement = current_db["accounts"][account_id]["statements"][period]
    return Result(
        value=f"Here is your bank statement for {period}:\n{statement}",
        agent=None  # Transfer back to triage in AgentSwarm
    )
