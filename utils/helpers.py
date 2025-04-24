from datetime import datetime
import random
import string

def get_current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def generate_bank_id(bank_name):
    prefix = bank_name.strip().upper()[:3]
    date_part = datetime.now().strftime("%Y%m%d")
    return f"{prefix}{date_part}"

def generate_staff_id(name):
    prefix = name.strip().upper()[:3]
    date_str = datetime.now().strftime("%m%d")
    random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
    return f"{prefix}{date_str}{random_suffix}"

def generate_account_id(name):
    date_str = datetime.now().strftime("%m%d")
    return name[:3].upper() + date_str

def generate_transaction_id(bank_id, account_id):
    return f"TXN{bank_id}{account_id}{datetime.now().strftime('%m%d%H%M%S')}"

def generate_currency_id(name):
    prefix = name.strip().upper()[:3]
    date_str = datetime.now().strftime("%m%d")
    return f"{prefix}{date_str}"

def generate_charges_id(bank_id):
    prefix = bank_id.strip().upper()[:3]
    date_str = datetime.now().strftime("%d%m")
    return f"{prefix}CHG{date_str}"
