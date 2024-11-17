from swarm import Swarm
from agents.triage_agent import TriageAgent
from agents.accounts_agent import AccountsAgent, handle_account_balance, retrieve_bank_statement
from agents.payments_agent import PaymentsAgent, transfer_funds, schedule_payment, cancel_payment
from utils.helpers import (
    validate_account_id, validate_payment_id, generate_payment_id,
    validate_amount, get_user_accounts
)
from dotenv import load_dotenv
import os
from openai import OpenAI
from typing import Dict, List, Tuple, Callable
import logging
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize OpenAI client if needed
client = Swarm()

class AgentSwarm:
    def __init__(self, socket):
        """
        Initialize the AgentSwarm with necessary agents and their corresponding functions.

        Args:
            socket: Handles real-time communication (e.g., sending messages).
        """
        self.socket = socket
        self.messages = []
        
        # Initialize Agents with their instructions and functions
        self.triage_agent = TriageAgent(
            transfer_to_accounts=self.transfer_to_accounts,
            transfer_to_payments=self.transfer_to_payments
        )
        
        self.accounts_agent = AccountsAgent(
            transfer_to_payments=self.transfer_to_payments,
            handle_account_balance=handle_account_balance,
            retrieve_bank_statement=retrieve_bank_statement
        )
        
        self.payments_agent = PaymentsAgent(
            transfer_back_to_triage=self.transfer_back_to_triage,
            transfer_funds=transfer_funds,
            schedule_payment=schedule_payment,
            cancel_payment=cancel_payment
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
        
        # Capture the assistant's response and append to messages
        bot_response = ""
        for chunk in response:
            if "content" in chunk and chunk['content']:
                yield chunk['content']
                bot_response += chunk['content']
        print()  # For newline after the response
        
        # Append the assistant's response to the message history
        if bot_response:
            self.messages.append({
                "role": "assistant",
                "content": bot_response
            })
