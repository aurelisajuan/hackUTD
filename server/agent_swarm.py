# agent_swarm.py
from agents.triage_agent import TriageAgent
from agents.accounts_agent import AccountsAgent, handle_account_balance, retrieve_bank_statement
from agents.payments_agent import PaymentsAgent, transfer_funds, schedule_payment, cancel_payment
from agents.applications_agent import ApplicationsAgent, apply_for_loan, apply_for_credit_card  # <-- New Import
from utils.helpers import (
    validate_account_id, validate_payment_id, generate_payment_id,
    validate_amount, get_user_accounts
)
from swarm import Swarm  # Assuming Swarm is defined in swarm/__init__.py
from dotenv import load_dotenv
import os
from openai import OpenAI
from typing import Dict, List
import logging
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the Swarm client
client = Swarm()

# Initialize OpenAI client if needed
openai_client = OpenAI()

# Define the OpenAI model you're using
OPENAI_MODEL = "gpt-4o-mini"  # Replace with your specific model if different

class AgentSwarm:
    def __init__(self, socket=None):
        """
        Initialize the AgentSwarm with necessary agents and their corresponding functions.

        Args:
            socket: Handles real-time communication (e.g., sending messages).
        """
        self.socket = socket
        self.messages = []
        
        # Initialize Agents with their instructions and functions, including the model
        self.triage_agent = TriageAgent(
            [self.transfer_to_accounts, self.transfer_to_payments, self.transfer_to_applications]  # Add transfer function
        )
        
        self.accounts_agent = AccountsAgent(
            transfer_to_payments=self.transfer_to_payments,
            handle_account_balance=handle_account_balance,
            retrieve_bank_statement=retrieve_bank_statement,
        )
        
        self.payments_agent = PaymentsAgent(
            transfer_back_to_triage=self.transfer_back_to_triage,
            transfer_funds=transfer_funds,
            schedule_payment=schedule_payment,
            cancel_payment=cancel_payment,
        )
        
        self.applications_agent = ApplicationsAgent(
            transfer_back_to_triage=self.transfer_back_to_triage,
            apply_for_loan=apply_for_loan,
            apply_for_credit_card=apply_for_credit_card,
        )
        
        self.current_agent = self.triage_agent

    # -------------------- Transfer Functions -------------------- #
    
    def transfer_to_accounts(self, context_variables: Dict, user_message: str):
        logging.info("Transferring to Accounts Agent.")
        self.current_agent = self.accounts_agent
        return self.accounts_agent
    
    def transfer_to_payments(self, context_variables: Dict, user_message: str):
        logging.info("Transferring to Payments Agent.")
        self.current_agent = self.payments_agent
        return self.payments_agent

    def transfer_to_applications(self, context_variables: Dict, user_message: str):
        logging.info("Transferring to Applications Agent.")
        self.current_agent = self.applications_agent
        return self.applications_agent
    
    def transfer_back_to_triage(self, context_variables: Dict, response: str):
        logging.info("Transferring back to Triage Agent.")
        self.current_agent = self.triage_agent
        return self.triage_agent
    
    # -------------------- Run Function -------------------- #
    
    def run(self, messages: List[Dict[str, str]], stream: bool = False):
        """
        Executes the swarm by running the Triage Agent with the provided messages.
        
        Args:
            messages (List[Dict[str, str]]): List of messages to process.
            stream (bool): Whether to stream the response.
        
        Yields:
            str: The assistant's response chunks.
        """
        # Append new messages to internal message history
        self.messages.extend(messages)
        logging.info(f"Current message history: {self.messages}")
        
        # Run the swarm with the accumulated messages
        response = client.run(
            agent=self.current_agent,
            messages=self.messages,
            stream=stream
        )

        return response