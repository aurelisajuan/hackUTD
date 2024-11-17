from swarm import Agent, Swarm
from dotenv import load_dotenv
import os
import math
load_dotenv()
from openai import OpenAI
openai_client = OpenAI()

client = Swarm()

triage_instructions = f"""
You are to triage a users request, and call a tool to transfer to the right intent.
Once you are ready to transfer to the right intent, call the tool to transfer to the right intent.
You dont need to know specifics, just the topic of the request.
If the user request is about their account, transfer to the Accounts Agent.
If the user request is about any form of payment, transfer to the Payments Agent.
When you need more information to triage the request to an agent, ask a direct question without explaining why you're asking it.
Do not share your thought process with the user! Do not make unreasonable assumptions on behalf of user.
Upon transferring to a different agent, please send another message confirming you are the requested agent.
"""

accounts_instructions = f"""
You are a highly knowledgeable, professional, and user-friendly banking virtual agent. 
Your primary task is to assist users with account-related requests, such as checking account balances, retrieving bank statements, and answering questions about their accounts. 
Please maintain a polite and empathetic tone.
When asked a question related to accounts (such as balances, transactions, etc), please call the get_account_info function, which will return a dictionary of account information. Use this information to provide the best answer to the user's request.
"""

payments_instructions = f"""
You are a virtual banking agent designed to assist users with payment-related requests. 
Your primary focus is facilitating secure and accurate money transfers, including transferring funds between the user's accounts, 
sending money to others, and scheduling or canceling payments. 
Please maintain a polite and empathetic tone, and provide user-friendly instructions.
"""

class AgentSwarm:
  def __init__(self):
    self.triage_agent = Agent(
      name="Triage Agent",
      instructions=triage_instructions,
      functions=[self.transfer_to_accounts, self.transfer_to_payments],
    )

    self.accounts = Agent(
      name="accounts",
      instructions=accounts_instructions,
    )

    self.payments = Agent(
      name="payments",
      instructions=payments_instructions,
    )

    self.accounts.functions = [self.transfer_back_to_triage]
    self.payments.functions = [self.transfer_back_to_triage]

    self.current_agent = self.triage_agent

  # Transfer functions
  def transfer_to_accounts(self):
    print("transferring to accounts")
    self.current_agent = self.accounts

  def transfer_to_payments(self):
    self.current_agent = self.payments
  
  def transfer_back_to_triage(self):
    self.current_agent = self.triage_agent

  def run(self, messages, stream=False):
    response = client.run(
      agent=self.current_agent,
      messages=messages,
      stream=stream
    )
    return response