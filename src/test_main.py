import pytest
from unittest.mock import mock_open, patch
from main import mask_card_number, mask_account_number, format_date, get_digits, clean_up_digits, load_transactions, sort_transactions

# Тесты для функции mask_account_number
@pytest.mark.parametrize("account_number, expected", [
    ("Invalid Account Number", "N/A"),
    ("1234", "**1234"),
    ("12345", "**2345"),
    ("Account 12345", "Account **2345"),
    ("123456789987654321", "**4321"),
])
def test_mask_account_number(account_number, expected):
    assert mask_account_number(account_number) == expected

# Тесты для функции mask_card_number
@pytest.mark.parametrize("card_info, expected_masked_number", [
    ("Visa 1234567812345678", "Visa 1234 56** **** 5678"),
    ("MasterCard 9876543210987654", "MasterCard 9876 54** **** 7654"),
    ("", "N/A"),
    ("American Express 12345678", "N/A"),
])
def test_mask_card_number(card_info, expected_masked_number):
    assert mask_card_number(card_info) == expected_masked_number

# Тесты для функции format_date
@pytest.mark.parametrize("date_str, expected_formatted_date", [
    ("2023-12-31T23:59:59.999", "31.12.2023"),
    ("2024-03-15T12:30:00.000", "15.03.2024"),
])
def test_format_date(date_str, expected_formatted_date):
    assert format_date(date_str) == expected_formatted_date

# Тесты для функции get_digits
@pytest.mark.parametrize("info, expected_info", [
    ("", ""),
    ("abc", ""),
    ("a1b", "1"),
    ("123", "123"),
    ("123 456", "123456"),
    ("123 a1b 456", "1231456"),
])
def test_get_digits(info, expected_info):
    assert get_digits(info) == expected_info

# Тесты для функции clean_up_digits
@pytest.mark.parametrize("info, expected_info", [
    ("", ""),
    ("124", ""),
    ("1a4", "a"),
    ("abc", "abc"),
    ("abc def", "abc def"),
])
def test_clean_up_digits(info, expected_info):
    assert clean_up_digits(info) == expected_info

# Тесты для функции load_transactions
@patch('builtins.open', new_callable=mock_open, read_data='[{"state": "EXECUTED", "date": "2023-03-25T12:34:56.789"}]')
def test_load_transactions(mock_file):
    transactions = load_transactions('test.json')
    assert transactions == [{"state": "EXECUTED", "date": "2023-03-25T12:34:56.789"}]

# Тесты для функции sort_transactions
def test_sort_transactions():
    transactions = [
        {"state": "EXECUTED", "date": "2023-03-25T12:34:56.789"},
        {"state": "EXECUTED", "date": "2023-03-24T09:10:11.123"},
        {"state": "EXECUTED", "date": "2023-03-26T15:16:17.456"},
        {"state": "PENDING", "date": "2023-03-25T18:19:20.789"}
    ]
    expected_sorted_transactions = [
        {"state": "EXECUTED", "date": "2023-03-26T15:16:17.456"},
        {"state": "EXECUTED", "date": "2023-03-25T12:34:56.789"},
        {"state": "EXECUTED", "date": "2023-03-24T09:10:11.123"}
    ]
    sorted_transactions = sort_transactions(transactions)
    assert sorted_transactions == expected_sorted_transactions[:5]