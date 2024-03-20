import json
from datetime import datetime

def mask_card_number(card_info):
    # Разделяем название карты и номер
    card_parts = card_info.split()
    if len(card_parts) < 2:
        return "N/A"

    # Записываем название карты полностью
    card_type = ' '.join(card_parts[:-1])

    # Маскируем номер карты
    card_number = card_parts[-1]
    if len(card_number) >= 12:
        masked_number = card_number[:4] + ' ' + '*' * 4 + ' ' + '*' * 4 + ' ' + card_number[-4:]
        return f"{card_type} {masked_number}"
    return "N/A"

def mask_account_number(account_number):
    # Проверяем, что номер счета не является пустой строкой и его длина больше или равна 4
    if account_number and len(account_number) >= 4:
        return f"**{account_number[-4:]}"
    else:
        return "N/A"

def format_date(date_str):
    # Попробуем распарсить дату, если возможно
    try:
        date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f')
        return date.strftime('%d.%m.%Y')
    except ValueError:
        return "N/A"

def process_transactions(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Фильтрация и сортировка транзакций
    executed_transactions = [t for t in data if t.get('state') == 'EXECUTED']
    sorted_transactions = sorted(executed_transactions,
                                 key=lambda t: datetime.strptime(t.get('date'), '%Y-%m-%dT%H:%M:%S.%f'), reverse=True)[:5]

    for transaction in sorted_transactions:
        date = format_date(transaction.get('date'))
        description = transaction.get('description', "N/A")
        from_account = transaction.get('from', "N/A")
        to_account = transaction.get('to', "N/A")
        amount = transaction.get('operationAmount', {}).get('amount', "N/A")
        currency = transaction.get('operationAmount', {}).get('currency', {}).get('name', "N/A")

        # Маскировка номеров счетов и карт
        masked_from_account = mask_card_number(from_account) if 'from' in transaction else mask_account_number(from_account)
        masked_to_account = mask_account_number(to_account)

        # Вывод транзакции
        print(f"{date} {description}")
        print(f"{masked_from_account} -> Счет {masked_to_account}")
        print(f"{amount} {currency}")
        print()  # Пустая строка для разделения операций

if __name__ == "__main__":
    file_path = "operations.json"
    process_transactions(file_path)
