import json

def process_transactions(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    for transaction in data:
        print(f"Transaction ID: {transaction['id']}")
        print(f"Date: {transaction['date']}")
        print(f"State: {transaction['state']}")
        print(f"Operation Amount: {transaction['operationAmount']}")
        print(f"Description: {transaction['description']}")
        print(f"From: {transaction.get('from', 'N/A')}")
        print(f"To: {transaction['to']}")
        print("\n")

if __name__ == "__main__":
    # Измените путь к файлу на вашем компьютере
    file_path = r"C:\Users\ivani\OneDrive\Рабочий стол\Гладченко И Г\operations (1).json"
    process_transactions(file_path)
