# db.py
from datetime import datetime, timedelta
import random

# Initial Banking Database Structure
db = {
    "users": {
        "user1": {"name": "John Doe", "accounts": ["ACC123", "ACC456"]},
        "user2": {"name": "Jane Smith", "accounts": ["ACC789"]},
    },
    "accounts": {
        "ACC123": {
            "balance": 2500.00,
            "statements": {
                "January": "Transaction 1: -$500.00\nTransaction 2: +$1500.00",
                "February": "Transaction 1: -$300.00\nTransaction 2: +$800.00",
            },
        },
        "ACC456": {
            "balance": 1000.00,
            "statements": {
                "January": "Transaction 1: -$200.00\nTransaction 2: +$1200.00",
                "February": "Transaction 1: -$100.00\nTransaction 2: +$500.00",
            },
        },
        "ACC789": {
            "balance": 5000.00,
            "statements": {
                "January": "Transaction 1: -$1000.00\nTransaction 2: +$2000.00",
                "February": "Transaction 1: -$500.00\nTransaction 2: +$1500.00",
            },
        },
    },
    "payments": {
        "PAY001": {
            "from_account": "ACC123",
            "to_account": "ACC456",
            "amount": 300.00,
            "date": "2024-05-01",
            "status": "Scheduled",
        },
        "PAY002": {
            "from_account": "ACC456",
            "to_account": "ACC123",
            "amount": 150.00,
            "date": "2024-05-15",
            "status": "Completed",
        },
    },
}

calls_db = {}


def generate_sample_data():
    sample_data = [
        {
            "id": "1",
            "time": (
                datetime.now() - timedelta(minutes=random.randint(0, 120))
            ).isoformat(),
            "transcript": [
                {
                    "role": "assistant",
                    "content": "Hello, welcome to TalkTuahBank. How can I help you today?",
                },
                {
                    "role": "user",
                    "content": "Hi, I'd like to check my account balance please",
                },
                {
                    "role": "assistant",
                    "content": "I'd be happy to help you check your balance. Could you please verify your account number?",
                },
                {"role": "user", "content": "Yes, it's ACC123"},
            ],
            "user_id": "user1",
            "referenced_documents": [],
        },
        {
            "id": "2",
            "time": (
                datetime.now() - timedelta(minutes=random.randint(0, 120))
            ).isoformat(),
            "transcript": [
                {
                    "role": "assistant",
                    "content": "Hello, welcome to TalkTuahBank. How can I help you today?",
                },
                {"role": "user", "content": "I need to make a payment to someone"},
                {
                    "role": "assistant",
                    "content": "I can help you with making a payment. Could you tell me who you'd like to send money to?",
                },
                {"role": "user", "content": "I want to send $50 to my friend John"},
            ],
            "user_id": "user2",
            "referenced_documents": [],
        },
        {
            "id": "3",
            "time": (
                datetime.now() - timedelta(minutes=random.randint(0, 120))
            ).isoformat(),
            "transcript": [
                {
                    "role": "assistant",
                    "content": "Hello, welcome to TalkTuahBank. How can I help you today?",
                },
                {"role": "user", "content": "I lost my credit card"},
                {
                    "role": "assistant",
                    "content": "I'm sorry to hear that. I'll help you report your lost card right away. First, can you verify your identity?",
                },
                {"role": "user", "content": "Yes, my account number is ACC456"},
            ],
            "user_id": "user3",
            "referenced_documents": [],
        },
        {
            "id": "4",
            "time": (
                datetime.now() - timedelta(minutes=random.randint(0, 120))
            ).isoformat(),
            "transcript": [
                {
                    "role": "assistant",
                    "content": "Hello, welcome to TalkTuahBank. How can I help you today?",
                },
                {"role": "user", "content": "I'd like to see my recent transactions"},
                {
                    "role": "assistant",
                    "content": "I can help you review your recent transactions. Could you please provide your account number?",
                },
                {"role": "user", "content": "It's ACC789"},
            ],
            "user_id": "user4",
            "referenced_documents": [],
        },
        {
            "id": "5",
            "time": (
                datetime.now() - timedelta(minutes=random.randint(0, 120))
            ).isoformat(),
            "transcript": [
                {
                    "role": "assistant",
                    "content": "Hello, welcome to TalkTuahBank. How can I help you today?",
                },
                {"role": "user", "content": "I need help with my mortgage payment"},
                {
                    "role": "assistant",
                    "content": "I'll be happy to assist you with your mortgage payment. What specific information do you need?",
                },
                {
                    "role": "user",
                    "content": "I want to know when my next payment is due",
                },
            ],
            "user_id": "user5",
            "referenced_documents": [],
        },
    ]
    for call in sample_data:
        calls_db[call["id"]] = call
    return sample_data


generate_sample_data()


def get_db():
    """
    Retrieves the current state of the banking database.

    Returns:
        dict: The current banking database dictionary.
    """
    return db


def set_db(new_db):
    """
    Updates the banking database with a new state.

    Args:
        new_db (dict): The new banking database dictionary to replace the current state.

    Returns:
        bool: True if the database was successfully updated.
    """
    global db
    db = new_db
    return True


def get_all_calls():
    """
    Accessor function to get all calls in the database.
    """
    return calls_db


def get_call(call_id):
    """
    Accessor function to get a specific call by its ID.
    """
    return calls_db.get(call_id, {})


def update_call(call_id, updated_data):
    """
    Modification function to update or insert a specific call's data.
    """
    if call_id in calls_db:
        calls_db[call_id].update(updated_data)
    else:
        calls_db[call_id] = updated_data
    return True


def delete_call(call_id):
    """
    Function to delete a call from the database.
    """
    if call_id in calls_db:
        del calls_db[call_id]
        return True
    return False
