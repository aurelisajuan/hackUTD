# agent_swarm.py

from swarm import Swarm, Agent
from swarm.types import Result
from dotenv import load_dotenv
import os
load_dotenv()
from openai import OpenAI
openai_client = OpenAI()
from typing import Dict, List, Tuple
from db import get_db, set_db  # Importing the banking db functions
import logging
from datetime import datetime
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the Swarm client
client = Swarm()

# Define instructions for each agent

triage_instructions = """
You are the Triage Agent responsible for categorizing user requests and delegating them to the appropriate agent.

Your tasks:
1. Analyze the user's message to determine its intent.
2. If the request is about account-related inquiries (e.g., checking balance, retrieving statements), transfer it to the Accounts Agent.
3. If the request is about payment-related actions (e.g., transferring funds, scheduling payments), transfer it to the Payments Agent.
4. If you need more information to accurately triage the request, ask a direct question without providing explanations.
5. Do not share your internal decision-making process with the user.
6. Maintain a professional and friendly tone at all times.
"""

accounts_instructions = """
You are the Accounts Agent, a highly knowledgeable and professional virtual banking assistant.

Your responsibilities include:
1. Assisting users with account-related requests, such as checking account balances and retrieving bank statements.
2. Answering questions about account features, services, and policies.
3. Ensuring compliance with financial regulations and maintaining customer privacy.
4. Communicating in a polite, empathetic, and user-friendly manner.
"""

payments_instructions = """
You are the Payments Agent, a virtual banking assistant specializing in payment-related requests.

Your duties involve:
1. Facilitating secure and accurate money transfers between user accounts.
2. Assisting with sending money to others, scheduling payments, and canceling transactions.
3. Following all banking security protocols to protect user information.
4. Providing clear, professional, and user-friendly instructions to users.
"""

# Define the AgentSwarm class

class AgentSwarm:
    def __init__(self, socket):
        """
        Initialize the AgentSwarm with necessary agents and their corresponding functions.
        
        Args:
            socket: Handles real-time communication (e.g., sending messages).
        """
        self.socket = socket
        self.messages = []  # Internal message history
        
        # Initialize Agents with their instructions and functions
        self.triage_agent = Agent(
            name="Triage Agent",
            instructions=triage_instructions,
            functions=[self.transfer_to_accounts, self.transfer_to_payments]
        )
        
        self.accounts_agent = Agent(
            name="Accounts Agent",
            instructions=accounts_instructions,
            functions=[self.transfer_to_payments, self.handle_account_balance, self.retrieve_bank_statement]
        )
        
        self.payments_agent = Agent(
            name="Payments Agent",
            instructions=payments_instructions,
            functions=[self.transfer_back_to_triage, self.transfer_funds, self.schedule_payment, self.cancel_payment]
        )
        
        self.current_agent = self.triage_agent
    
    # -------------------- Helper Functions -------------------- #
    
    # General Helper Functions
    
    def _validate_account_id(self, account_id: str) -> bool:
        """
        Validates that the provided account ID exists in the database.
        
        Args:
            account_id (str): The account ID to validate.
        
        Returns:
            bool: True if the account exists, False otherwise.
        """
        current_db = get_db()
        if account_id in current_db["accounts"]:
            logging.info(f"Account ID {account_id} is valid.")
            return True
        logging.warning(f"Account ID {account_id} is invalid.")
        return False
    
    def _validate_payment_id(self, payment_id: str) -> bool:
        """
        Validates that the provided payment ID exists in the database.
        
        Args:
            payment_id (str): The payment ID to validate.
        
        Returns:
            bool: True if the payment exists, False otherwise.
        """
        current_db = get_db()
        if payment_id in current_db["payments"]:
            logging.info(f"Payment ID {payment_id} is valid.")
            return True
        logging.warning(f"Payment ID {payment_id} is invalid.")
        return False
    
    def _generate_payment_id(self) -> str:
        """
        Generates a unique payment ID.
        
        Returns:
            str: A unique payment ID.
        """
        current_db = get_db()
        payment_number = len(current_db["payments"]) + 1
        payment_id = f"PAY{payment_number:03d}"
        logging.info(f"Generated new payment ID: {payment_id}")
        return payment_id
    
    def _validate_amount(self, amount: float) -> bool:
        """
        Validates that the amount is positive and within allowable limits.
        
        Args:
            amount (float): The amount to validate.
        
        Returns:
            bool: True if valid, False otherwise.
        """
        if amount <= 0:
            logging.warning(f"Invalid amount: {amount}. Amount must be positive.")
            return False
        # Additional validation rules can be added here
        logging.info(f"Amount {amount} is valid.")
        return True
    
    def _get_user_accounts(self, user_id: str) -> List[str]:
        """
        Retrieves the list of account IDs associated with a user.
        
        Args:
            user_id (str): The user's ID.
        
        Returns:
            List[str]: A list of account IDs.
        """
        current_db = get_db()
        accounts = current_db["users"].get(user_id, {}).get("accounts", [])
        logging.info(f"User {user_id} has accounts: {accounts}")
        return accounts
    
    # -------------------- Agent Functions -------------------- #
    
    # Transfer Functions
    
    def transfer_to_accounts(self, context_variables, user_message: str):
        """
        Transfers the conversation to the Accounts Agent.
        
        Args:
            context_variables: Current state of the database or context.
            user_message (str): The user's message to be processed.
        
        Returns:
            Agent: The Accounts Agent instance.
        """
        logging.info("Transferring to Accounts Agent.")
        self.current_agent = self.accounts_agent
        return self.accounts_agent
    
    def transfer_to_payments(self, context_variables, user_message: str):
        """
        Transfers the conversation to the Payments Agent.
        
        Args:
            context_variables: Current state of the database or context.
            user_message (str): The user's message to be processed.
        
        Returns:
            Agent: The Payments Agent instance.
        """
        logging.info("Transferring to Payments Agent.")
        self.current_agent = self.payments_agent
        return self.payments_agent
    
    def transfer_back_to_triage(self, context_variables, response: str):
        """
        Transfers the conversation back to the Triage Agent after completing a task or if you are unable to complete the task.
        
        Args:
            context_variables: Current state of the database or context.
            response (str): The response generated by the current agent.
        
        Returns:
            Agent: The Triage Agent instance.
        """
        logging.info("Transferring back to Triage Agent.")
        return self.triage_agent
    
    # -------------------- Accounts Agent Functions -------------------- #
    
    def handle_account_balance(self, context_variables, account_id: str):
        """
        Handles requests to check account balances.
        
        Args:
            context_variables: Current state of the database or context.
            account_id (str): The user's account identifier.
        
        Returns:
            Result: Contains the account balance information.
        """
        logging.info(f"Handling account balance for account ID: {account_id}")
        if not self._validate_account_id(account_id):
            return Result(
                value="Invalid account ID provided.",
                agent=self.triage_agent
            )
        
        current_db = get_db()
        balance = current_db["accounts"][account_id]["balance"]
        return Result(
            value=f"Your current account balance for {account_id} is ${balance:.2f}.",
            agent=self.triage_agent  # Transfer back to Triage after handling
        )
    
    def retrieve_bank_statement(self, context_variables, account_id: str, period: str):
        """
        Retrieves bank statements for a given account and period.
        
        Args:
            context_variables: Current state of the database or context.
            account_id (str): The user's account identifier.
            period (str): The period for which to retrieve the statement (e.g., 'January', 'February').
        
        Returns:
            Result: Contains the bank statement information.
        """
        logging.info(f"Retrieving bank statement for account ID: {account_id}, period: {period}")
        if not self._validate_account_id(account_id):
            return Result(
                value="Invalid account ID provided.",
                agent=self.triage_agent
            )
        
        current_db = get_db()
        
        # Validate period
        if period not in current_db["accounts"][account_id]["statements"]:
            return Result(
                value=f"No statements found for the period: {period}.",
                agent=self.triage_agent
            )
        
        statement = current_db["accounts"][account_id]["statements"][period]
        return Result(
            value=f"Here is your bank statement for {period}:\n{statement}",
            agent=self.triage_agent  # Transfer back to Triage after handling
        )
    
    # -------------------- Payments Agent Functions -------------------- #
    
    def transfer_funds(self, context_variables, from_account: str, to_account: str, amount: float):
        """
        Facilitates the transfer of funds between accounts.
        
        Args:
            context_variables: Current state of the database or context.
            from_account (str): The account to transfer funds from.
            to_account (str): The account to transfer funds to.
            amount (float): The amount to transfer.
        
        Returns:
            Result: Confirmation of the fund transfer.
        """
        logging.info(f"Transferring funds from {from_account} to {to_account} amount: ${amount}")
        
        # Validate accounts
        if not self._validate_account_id(from_account):
            return Result(
                value=f"Source account ID {from_account} does not exist.",
                agent=self.triage_agent
            )
        if not self._validate_account_id(to_account):
            return Result(
                value=f"Destination account ID {to_account} does not exist.",
                agent=self.triage_agent
            )
        
        # Validate amount
        if not self._validate_amount(amount):
            return Result(
                value="The transfer amount must be a positive number.",
                agent=self.triage_agent
            )
        
        current_db = get_db()
        
        # Check for sufficient funds
        if current_db["accounts"][from_account]["balance"] < amount:
            return Result(
                value="Insufficient funds in the source account.",
                agent=self.triage_agent
            )
        
        # Perform the transfer
        current_db["accounts"][from_account]["balance"] -= amount
        current_db["accounts"][to_account]["balance"] += amount
        
        # Record the payment
        new_payment_id = self._generate_payment_id()
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
            agent=self.triage_agent  # Transfer back to Triage after handling
        )
    
    def schedule_payment(self, context_variables, account_id: str, payee: str, amount: float, date: str):
        """
        Schedules a future payment.
        
        Args:
            context_variables: Current state of the database or context.
            account_id (str): The user's account identifier.
            payee (str): The recipient of the payment.
            amount (float): The amount to be paid.
            date (str): The date when the payment should be made.
        
        Returns:
            Result: Confirmation of the scheduled payment.
        """
        logging.info(f"Scheduling payment of ${amount} to {payee} on {date} from {account_id}")
        
        # Validate account
        if not self._validate_account_id(account_id):
            return Result(
                value="Invalid account ID provided.",
                agent=self.triage_agent
            )
        
        # Validate amount
        if not self._validate_amount(amount):
            return Result(
                value="The payment amount must be a positive number.",
                agent=self.triage_agent
            )
        
        current_db = get_db()
        
        # Check for sufficient funds
        if current_db["accounts"][account_id]["balance"] < amount:
            return Result(
                value="Insufficient funds in the account to schedule this payment.",
                agent=self.triage_agent
            )
        
        # Deduct amount from account (assuming scheduling holds the funds)
        current_db["accounts"][account_id]["balance"] -= amount
        
        # Generate payment ID and schedule the payment
        new_payment_id = self._generate_payment_id()
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
            agent=self.triage_agent  # Transfer back to Triage after handling
        )
    
    def cancel_payment(self, context_variables, payment_id: str):
        """
        Cancels a scheduled payment.
        
        Args:
            context_variables: Current state of the database or context.
            payment_id (str): The identifier of the payment to cancel.
        
        Returns:
            Result: Confirmation of the cancellation.
        """
        logging.info(f"Cancelling payment with ID: {payment_id}")
        
        # Validate payment_id
        if not self._validate_payment_id(payment_id):
            return Result(
                value=f"Payment ID {payment_id} does not exist.",
                agent=self.triage_agent
            )
        
        current_db = get_db()
        
        # Check payment status
        if current_db["payments"][payment_id]["status"] != "Scheduled":
            return Result(
                value=f"Payment ID {payment_id} cannot be canceled as it is already {current_db['payments'][payment_id]['status']}.",
                agent=self.triage_agent
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
            agent=self.triage_agent  # Transfer back to Triage after handling
        )
    
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
