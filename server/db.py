# db.py
from datetime import datetime, timedelta
import random

# Initial Banking Database Structure
db = {
    "users": {
        "+14085858267": {
            "name": "Bill Zhang",
            "accounts": ["ACC892", "ACC347"],
            "ssn": "784-29-5163",
            "address": "4728 Willow Creek Rd, Austin, TX 78701",
            "date_of_birth": "1991-08-24",
            "email": "bill.zhang@outlook.com",
            "phone": "+1-408-585-8267",
        },
        "+19178286465": {
            "name": "Warren Yun",
            "accounts": ["ACC123", "ACC456"],
            "ssn": "123-45-6789",
            "address": "123 Main St, Dallas, TX 75201",
            "date_of_birth": "1985-03-15",
            "email": "warren.yun@email.com",
            "phone": "+1-917-828-6465",
        },
        "+14695550456": {
            "name": "Jane Smith",
            "accounts": ["ACC789", "ACC790", "ACC791"],
            "ssn": "987-65-4321",
            "address": "456 Oak Ave, Plano, TX 75024",
            "date_of_birth": "1990-07-22",
            "email": "jane.smith@email.com",
            "phone": "+1-469-555-0456",
        },
        "+1-972-555-0789": {
            "name": "Michael Johnson",
            "accounts": ["ACC321", "ACC322"],
            "ssn": "456-78-9012",
            "address": "789 Elm St, Richardson, TX 75080",
            "date_of_birth": "1988-11-30",
            "email": "michael.j@email.com",
            "phone": "+1-972-555-0789",
        },
        "+1-817-555-0321": {
            "name": "Sarah Williams",
            "accounts": ["ACC654", "ACC655", "ACC656"],
            "ssn": "234-56-7890",
            "address": "321 Pine Rd, Fort Worth, TX 76102",
            "date_of_birth": "1992-04-18",
            "email": "sarah.w@email.com",
            "phone": "+1-817-555-0321",
        },
        "+1-214-555-0654": {
            "name": "David Brown",
            "accounts": ["ACC987", "ACC988"],
            "ssn": "345-67-8901",
            "address": "654 Maple Dr, Frisco, TX 75034",
            "date_of_birth": "1983-09-25",
            "email": "david.b@email.com",
            "phone": "+1-214-555-0654",
        },
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
        "ACC790": {
            "balance": 12500.00,
            "statements": {
                "January": "Transaction 1: -$2000.00\nTransaction 2: +$5000.00",
                "February": "Transaction 1: -$1500.00\nTransaction 2: +$3000.00",
            },
        },
        "ACC791": {
            "balance": 8000.00,
            "statements": {
                "January": "Transaction 1: -$1000.00\nTransaction 2: +$2500.00",
                "February": "Transaction 1: -$800.00\nTransaction 2: +$1800.00",
            },
        },
        "ACC892": {
            "balance": 3750.00,
            "statements": {
                "January": "Transaction 1: -$800.00\nTransaction 2: +$2500.00",
                "February": "Transaction 1: -$450.00\nTransaction 2: +$1200.00",
            },
        },
        "ACC347": {
            "balance": 8200.00,
            "statements": {
                "January": "Transaction 1: -$1500.00\nTransaction 2: +$3000.00",
                "February": "Transaction 1: -$700.00\nTransaction 2: +$2100.00",
            },
        },
        "ACC321": {
            "balance": 15000.00,
            "statements": {
                "January": "Transaction 1: -$3000.00\nTransaction 2: +$5000.00",
                "February": "Transaction 1: -$2000.00\nTransaction 2: +$4000.00",
            },
        },
        "ACC322": {
            "balance": 6500.00,
            "statements": {
                "January": "Transaction 1: -$1200.00\nTransaction 2: +$2800.00",
                "February": "Transaction 1: -$900.00\nTransaction 2: +$1600.00",
            },
        },
        "ACC654": {
            "balance": 9800.00,
            "statements": {
                "January": "Transaction 1: -$1800.00\nTransaction 2: +$3500.00",
                "February": "Transaction 1: -$1200.00\nTransaction 2: +$2500.00",
            },
        },
        "ACC655": {
            "balance": 4200.00,
            "statements": {
                "January": "Transaction 1: -$900.00\nTransaction 2: +$1500.00",
                "February": "Transaction 1: -$600.00\nTransaction 2: +$1200.00",
            },
        },
        "ACC656": {
            "balance": 7500.00,
            "statements": {
                "January": "Transaction 1: -$1500.00\nTransaction 2: +$2800.00",
                "February": "Transaction 1: -$1000.00\nTransaction 2: +$2000.00",
            },
        },
        "ACC987": {
            "balance": 11000.00,
            "statements": {
                "January": "Transaction 1: -$2500.00\nTransaction 2: +$4500.00",
                "February": "Transaction 1: -$1800.00\nTransaction 2: +$3200.00",
            },
        },
        "ACC988": {
            "balance": 5800.00,
            "statements": {
                "January": "Transaction 1: -$1200.00\nTransaction 2: +$2200.00",
                "February": "Transaction 1: -$800.00\nTransaction 2: +$1500.00",
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
        "PAY003": {
            "from_account": "ACC789",
            "to_account": "ACC892",
            "amount": 500.00,
            "date": "2024-04-30",
            "status": "Completed",
        },
        "PAY004": {
            "from_account": "ACC892",
            "to_account": "ACC347",
            "amount": 750.00,
            "date": "2024-05-10",
            "status": "Pending",
        },
        "PAY005": {
            "from_account": "ACC347",
            "to_account": "ACC789",
            "amount": 1000.00,
            "date": "2024-05-20",
            "status": "Scheduled",
        },
        "PAY006": {
            "from_account": "ACC123",
            "to_account": "ACC789",
            "amount": 250.00,
            "date": "2024-04-25",
            "status": "Completed",
        },
        "PAY007": {
            "from_account": "ACC790",
            "to_account": "ACC321",
            "amount": 1500.00,
            "date": "2024-05-05",
            "status": "Completed",
        },
        "PAY008": {
            "from_account": "ACC321",
            "to_account": "ACC654",
            "amount": 2000.00,
            "date": "2024-05-12",
            "status": "Pending",
        },
        "PAY009": {
            "from_account": "ACC655",
            "to_account": "ACC987",
            "amount": 800.00,
            "date": "2024-05-18",
            "status": "Scheduled",
        },
        "PAY010": {
            "from_account": "ACC988",
            "to_account": "ACC791",
            "amount": 1200.00,
            "date": "2024-04-28",
            "status": "Completed",
        },
    },
}

calls_db = {}


def generate_sample_data():
    sample_data = [
        {
            "id": "+1-214-555-0123",
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
            "user_id": "+1-214-555-0123",
            "referenced_documents": [],
        },
        {
            "id": "+1-469-555-0456",
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
            "user_id": "+1-469-555-0456",
            "referenced_documents": [],
        },
        {
            "id": "+1-972-555-0789",
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
            "user_id": "+1-972-555-0789",
            "referenced_documents": [],
        },
        {
            "id": "+1-817-555-0321",
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
            "user_id": "+1-817-555-0321",
            "referenced_documents": [],
        },
        {
            "id": "+1-214-555-0654",
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
            "user_id": "+1-214-555-0654",
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
