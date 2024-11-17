# agents/payments_agent.py

from .base_agent import BaseAgent
from typing import Any, Dict
from utils.helpers import (
    validate_account_id,
    validate_payment_id,
    generate_payment_id,
    validate_amount,
    get_db,
    set_db
)
from typing import Callable
from swarm.types import Result
import logging
from datetime import datetime

# Define the payments instructions
payments_instructions = """
You are the Payments Agent, a virtual banking assistant specializing in payment-related requests.

Your duties involve:
1. Facilitating secure and accurate money transfers between user accounts.
2. Assisting with sending money to others, scheduling payments, and canceling transactions.
3. Following all banking security protocols to protect user information.
4. Providing clear, professional, and user-friendly instructions to users.
"""

class PaymentsAgent(BaseAgent):
    def __init__(
        self,
        transfer_back_to_triage: Callable,
        transfer_funds: Callable,
        schedule_payment: Callable,
        cancel_payment: Callable
    ):
        super().__init__(
            name="Payments Agent",
            instructions=payments_instructions,
            functions=[transfer_back_to_triage, transfer_funds, schedule_payment, cancel_payment]
        )

# Define specific functions for Payments Agent

def transfer_funds(context_variables: Dict, from_account: str, to_account: str, amount: float) -> Result:
    logging.info(f"Transferring funds from {from_account} to {to_account} amount: ${amount}")
    
    # Validate accounts
    if not validate_account_id(from_account):
        return Result(
            value=f"Source account ID {from_account} does not exist.",
            agent=None  # Transfer back to triage in AgentSwarm
        )
    if not validate_account_id(to_account):
        return Result(
            value=f"Destination account ID {to_account} does not exist.",
            agent=None  # Transfer back to triage in AgentSwarm
        )
    
    # Validate amount
    if not validate_amount(amount):
        return Result(
            value="The transfer amount must be a positive number.",
            agent=None  # Transfer back to triage in AgentSwarm
        )
    
    current_db = get_db()
    
    # Check for sufficient funds
    if current_db["accounts"][from_account]["balance"] < amount:
        return Result(
            value="Insufficient funds in the source account.",
            agent=None  # Transfer back to triage in AgentSwarm
        )
    
    # Perform the transfer
    current_db["accounts"][from_account]["balance"] -= amount
    current_db["accounts"][to_account]["balance"] += amount
    
    # Record the payment
    new_payment_id = generate_payment_id()
    current_db["payments"][new_payment_id] = {
        "from_account": from_account,
        "to_account": to_account,
        "amount": amount,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "status": "Completed"
    }
    
    set_db(current_db)  # Update the database
    
    return Result(
        value=f"Successfully transferred ${amount:.2f} from {from_account} to {to_account}. Payment ID: {new_payment_id}.",
        agent=None  # Transfer back to triage in AgentSwarm
    )

def schedule_payment(context_variables: Dict, account_id: str, payee: str, amount: float, date: str) -> Result:
    logging.info(f"Scheduling payment of ${amount} to {payee} on {date} from {account_id}")
    
    # Validate account
    if not validate_account_id(account_id):
        return Result(
            value="Invalid account ID provided.",
            agent=None  # Transfer back to triage in AgentSwarm
        )
    
    # Validate amount
    if not validate_amount(amount):
        return Result(
            value="The payment amount must be a positive number.",
            agent=None  # Transfer back to triage in AgentSwarm
        )
    
    current_db = get_db()
    
    # Check for sufficient funds
    if current_db["accounts"][account_id]["balance"] < amount:
        return Result(
            value="Insufficient funds in the account to schedule this payment.",
            agent=None  # Transfer back to triage in AgentSwarm
        )
    
    # Deduct amount from account (assuming scheduling holds the funds)
    current_db["accounts"][account_id]["balance"] -= amount
    
    # Generate payment ID and schedule the payment
    new_payment_id = generate_payment_id()
    current_db["payments"][new_payment_id] = {
        "from_account": account_id,
        "to_account": payee,  
        "amount": amount,
        "date": date,
        "status": "Scheduled"
    }
    
    set_db(current_db) 
    
    return Result(
        value=f"Payment of ${amount:.2f} to {payee} scheduled on {date}. Payment ID: {new_payment_id}.",
        agent=None  # Transfer back to triage in AgentSwarm
    )

def cancel_payment(context_variables: Dict, payment_id: str) -> Result:
    logging.info(f"Cancelling payment with ID: {payment_id}")
    
    # Validate payment_id
    if not validate_payment_id(payment_id):
        return Result(
            value=f"Payment ID {payment_id} does not exist.",
            agent=None  # Transfer back to triage in AgentSwarm
        )
    
    current_db = get_db()
    
    # Check payment status
    if current_db["payments"][payment_id]["status"] != "Scheduled":
        return Result(
            value=f"Payment ID {payment_id} cannot be canceled as it is already {current_db['payments'][payment_id]['status']}.",
            agent=None  # Transfer back to triage in AgentSwarm
        )
    
    # Cancel the payment
    current_db["payments"][payment_id]["status"] = "Canceled"
    
    # Refund the amount back to the account
    from_account = current_db["payments"][payment_id]["from_account"]
    amount = current_db["payments"][payment_id]["amount"]
    current_db["accounts"][from_account]["balance"] += amount
    
    set_db(current_db)  # Update the database
    
    return Result(
        value=f"Payment with ID {payment_id} has been successfully canceled and ${amount:.2f} has been refunded to {from_account}.",
        agent=None  # Transfer back to triage in AgentSwarm
    )
