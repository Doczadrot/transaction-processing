import unittest
from unittest.mock import patch
from src.main import process_transactions

class TestTransactionProcessing(unittest.TestCase):
    def test_process_transactions(self):
        file_path = "path/to/test/data.json"
        test_data = [
            {"id": 1, "date": "2024-01-20", "state": "EXECUTED", "operationAmount": 100.0, "description": "Payment", "from": "A", "to": "B"},
            {"id": 2, "date": "2024-01-21", "state": "CANCELED", "operationAmount": 50.0, "description": "Refund", "from": "C", "to": "D"}
        ]

        with patch('builtins.open', return_value=test_data):
            process_transactions(file_path)

if __name__ == "__main__":
    unittest.main()