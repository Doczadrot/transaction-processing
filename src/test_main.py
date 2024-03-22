import json
import pytest
from main import mask_card_number, mask_account_number, format_date, get_digits, clean_up_digits

@pytest.mark.parametrize("account_number, expected", [
    ("Invalid Account Number", "N/A"),
    ("1234", "N/A"),
    ("12345", "*2345"),
    ("Account 12345", "Account *2345"),
    ("123456789987654321", "**************4321"),
])
def test_mask_account_number_invalid_format(account_number, expected):
    assert mask_account_number(account_number) == expected

@pytest.mark.parametrize("card_info, expected_masked_number", [
    ("Visa 1234567812345678", "Visa 1234 56** **** 5678"),
    ("MasterCard 9876543210987654", "MasterCard 9876 54** **** 7654"),
    ("", "N/A"),  # Тест на пустую строку
    ("American Express 12345678", "N/A"),  # Тест на неизвестный тип карты
])
def test_mask_card_number(card_info, expected_masked_number):
    assert mask_card_number(card_info) == expected_masked_number

@pytest.mark.parametrize("date_str, expected_formatted_date", [
    ("2023-12-31T23:59:59.999", "31.12.2023"),
    ("2024-03-15T12:30:00.000", "15.03.2024"),
])
def test_format_date(date_str, expected_formatted_date):
    assert format_date(date_str) == expected_formatted_date

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

@pytest.mark.parametrize("info, expected_info", [
    ("", ""),
    ("124", ""),
    ("1a4", "a"),
    ("abc", "abc"),
    ("abc def", "abc def")
    ])
def test_clean_up_digits(info, expected_info):
    assert clean_up_digits(info) == expected_info
