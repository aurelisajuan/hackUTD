# agents/triage_agent.py

from .base_agent import BaseAgent
from typing import Any, Dict
from typing import Callable
import logging

# Define the triage instructions
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

class TriageAgent(BaseAgent):
    def __init__(self, transfer_to_accounts: Callable, transfer_to_payments: Callable):
        super().__init__(
            name="Triage Agent",
            instructions=triage_instructions,
            functions=[transfer_to_accounts, transfer_to_payments]
        )
