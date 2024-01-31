import json

def mask_card_number(card_number):
    # Маскировка номера карты
    return f"{card_number[:6]} {'*'*4} {card_number[-4:]}"

def mask_account_number(account_number):
    # Маскировка номера счета
    return f"**{account_number[-4:]}"

def process_transactions(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Фильтрация и сортировка транзакций
    executed_transactions = [t for t in data if t.get('state') == 'EXECUTED']
    sorted_transactions = sorted(executed_transactions, key=lambda t: t.get('date'), reverse=True)[:5]

    for transaction in sorted_transactions:
        date = transaction.get('date', 'N/A').split('T')[0]
        description = transaction.get('description', 'N/A')
        from_account = transaction.get('from', 'N/A')
        to_account = transaction.get('to', 'N/A')
        amount = transaction.get('operationAmount', {}).get('amount', 'N/A')
        currency = transaction.get('operationAmount', {}).get('currency', {}).get('name', 'N/A')

        # Маскировка номеров счетов и карт
        masked_from_account = mask_card_number(from_account) if from_account else from_account
        masked_to_account = mask_account_number(to_account)

        # Вывод транзакции
        print(f"{date} {description}")
        print(f"{masked_from_account} -> Счет {masked_to_account}")
        print(f"{amount} {currency}\n")


if __name__ == "__main__":
    file_path = "operations.json"
    process_transactions(file_path)
