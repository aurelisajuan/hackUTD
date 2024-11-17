from swarm import Agent, Swarm
from dotenv import load_dotenv
import os
load_dotenv()
from openai import OpenAI
openai_client = OpenAI()

client = Swarm()

triage_instructions = f"""You are to triage a users request, and call a tool to transfer to the right intent.
            Once you are ready to transfer to the right intent, call the tool to transfer to the right intent.
            You dont need to know specifics, just the topic of the request.
            If the user request is about making an order or purchasing an item, transfer to the Sales Agent.
            If the user request is about getting a refund on an item or returning a product, transfer to the Refunds Agent.
            When you need more information to triage the request to an agent, ask a direct question without explaining why you're asking it.
            Do not share your thought process with the user! Do not make unreasonable assumptions on behalf of user.
            After transferring to a different agent, please send another message confirming you are the requested agent."""

accounts_instructions = f"""You are a highly knowledgeable, professional, and user-friendly banking virtual agent. Your primary task is to assist users with account-related requests, such as checking account balances, retrieving bank statements, and answering questions about their accounts. You strictly adhere to financial regulations, ensure customer privacy, and maintain a polite and empathetic tone."""
payments_instructions = f"""You are a virtual banking agent designed to assist users with payment-related requests. Your primary focus is facilitating secure and accurate money transfers, including transferring funds between the user's accounts, sending money to others, and scheduling or canceling payments. You follow all banking security protocols, ensure privacy, and provide clear, professional, and user-friendly instructions."""



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

    self.accounts.functions.append(self.transfer_back_to_triage)
    self.payments.functions.append(self.transfer_back_to_triage)


  def transfer_to_accounts(self):
    print("transferring to accounts")
    return self.accounts

  def transfer_to_payments(self):
    return self.payments
  
  def transfer_back_to_triage(self):
    return self.triage_agent
  
  def run(self, messages, stream=False):
    response = client.run(
      agent=self.triage_agent,
      messages=messages,
      stream=stream
    )
    return response