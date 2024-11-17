# db.py

# Initial Banking Database Structure
db = {
    "users": {
        "user1": {
            "name": "John Doe",
            "accounts": ["ACC123", "ACC456"]
        },
        "user2": {
            "name": "Jane Smith",
            "accounts": ["ACC789"]
        }
    },
    "accounts": {
        "ACC123": {
            "balance": 2500.00,
            "statements": {
                "January": "Transaction 1: -$500.00\nTransaction 2: +$1500.00",
                "February": "Transaction 1: -$300.00\nTransaction 2: +$800.00"
            }
        },
        "ACC456": {
            "balance": 1000.00,
            "statements": {
                "January": "Transaction 1: -$200.00\nTransaction 2: +$1200.00",
                "February": "Transaction 1: -$100.00\nTransaction 2: +$500.00"
            }
        },
        "ACC789": {
            "balance": 5000.00,
            "statements": {
                "January": "Transaction 1: -$1000.00\nTransaction 2: +$2000.00",
                "February": "Transaction 1: -$500.00\nTransaction 2: +$1500.00"
            }
        }
    },
    "payments": {
        "PAY001": {
            "from_account": "ACC123",
            "to_account": "ACC456",
            "amount": 300.00,
            "date": "2024-05-01",
            "status": "Scheduled"
        },
        "PAY002": {
            "from_account": "ACC456",
            "to_account": "ACC123",
            "amount": 150.00,
            "date": "2024-05-15",
            "status": "Completed"
        }
    }
}

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
