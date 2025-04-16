from datetime import datetime

def generate_bank_id(bank_name):
    prefix = bank_name.strip().upper()[:3]
    date_part = datetime.now().strftime("%Y%m%d")
    return f"{prefix}{date_part}"

def get_current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def generate_staff_id(staff_name, bank_name):
    # Get the first 3 letters of the staff's first name
    staff_name_parts = staff_name.split()
    staff_first_name = staff_name_parts[0][:3].upper()  # First three letters, capitalized

    # Get the first 3 letters of the bank's name
    bank_short_name = bank_name[:3].upper()  # First three letters, capitalized

    # Get today's date in MMDD format
    today_date = datetime.now().strftime("%m%d")  # MMDD format

    # Combine all parts to create the staff ID
    staff_id = staff_first_name + bank_short_name + today_date
    return staff_id

def generate_account_id(name):
    date_str = datetime.now().strftime("%m%d")
    return name[:3].upper() + date_str

def generate_transaction_id(bank_id, account_id):
    return f"TXN{bank_id}{account_id}{datetime.now().strftime('%m%d%H%M%S')}"