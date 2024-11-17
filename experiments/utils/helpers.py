# utils/helpers.py

from typing import List
from db import get_db, set_db
import logging
from datetime import datetime

def validate_account_id(account_id: str) -> bool:
    current_db = get_db()
    if account_id in current_db["accounts"]:
        logging.info(f"Account ID {account_id} is valid.")
        return True
    logging.warning(f"Account ID {account_id} is invalid.")
    return False

def validate_payment_id(payment_id: str) -> bool:
    current_db = get_db()
    if payment_id in current_db["payments"]:
        logging.info(f"Payment ID {payment_id} is valid.")
        return True
    logging.warning(f"Payment ID {payment_id} is invalid.")
    return False

def generate_payment_id() -> str:
    current_db = get_db()
    payment_number = len(current_db["payments"]) + 1
    payment_id = f"PAY{payment_number:03d}"
    logging.info(f"Generated new payment ID: {payment_id}")
    return payment_id

def validate_amount(amount: float) -> bool:
    if amount <= 0:
        logging.warning(f"Invalid amount: {amount}. Amount must be positive.")
        return False
    logging.info(f"Amount {amount} is valid.")
    return True

def get_user_accounts(user_id: str) -> List[str]:
    current_db = get_db()
    accounts = current_db["users"].get(user_id, {}).get("accounts", [])
    logging.info(f"User {user_id} has accounts: {accounts}")
    return accounts
