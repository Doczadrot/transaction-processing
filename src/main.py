import json
from datetime import datetime
import re

def get_digits(info):
    """returns digits from string"""
    mask = re.compile(r"\d+")
    digits = "".join(mask.findall(info))
    return digits.strip()

def clean_up_digits(info):
    """remove all digits from the string"""
    for i in range(10):
        info = info.replace(str(i), "")
    return info.strip()

def mask_card_number(card_info):
    digits = get_digits(card_info)
    if len(digits) < 12:
        return "N/A"
    card_info = clean_up_digits(card_info)
    blocks = [digits[i:i+4] for i in range(0, len(digits), 4)]

    blocks[1] = blocks[1][:2]+"**"
    for i in range(2, len(blocks)-1):
        blocks[i] = "****"
    blocks_str = " ".join(blocks)
    card = f"{card_info} {blocks_str}"
    return card


def mask_account_number(account_number):
    digits = get_digits(account_number)
    if len(digits) < 4:
        return "N/A"

    info = clean_up_digits(account_number)
    masked_number = f"{info} **{digits[-4:]}" if info else f"**{digits[-4:]}"

    return masked_number

def format_date(date_str):
    try:
        date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f')
        return date.strftime('%d.%m.%Y')
    except ValueError:
        return "N/A"

def process_transactions(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    executed_transactions = [t for t in data if t.get('state') == 'EXECUTED']
    sorted_transactions = sorted(executed_transactions,
                                 key=lambda t: datetime.strptime(t.get('date'), '%Y-%m-%dT%H:%M:%S.%f'), reverse=True)[:5]

    for transaction in sorted_transactions:
        date = format_date(transaction.get('date'))
        description = transaction.get('description', "N/A")
        from_account = transaction.get('from')
        to_account = transaction.get('to')
        amount = transaction.get('operationAmount', {}).get('amount', "N/A")
        currency = transaction.get('operationAmount', {}).get('currency', {}).get('name', "N/A")

        masked_from_account = mask_card_number(from_account) if from_account else "N/A"
        masked_to_account = mask_account_number(to_account) if to_account else "N/A"

        print(f"{date} {description}")
        print(f"{masked_from_account} -> {masked_to_account}")
        print(f"{amount} {currency}")
        print()

if __name__ == "__main__":
    file_path = "operations.json"
    process_transactions(file_path)
