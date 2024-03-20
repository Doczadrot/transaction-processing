import json
import pytest
from main import mask_card_number, mask_account_number, format_date

@pytest.mark.parametrize("account_number", [
    "Invalid Account Number",
])
def test_mask_account_number_invalid_format(account_number):
    assert mask_account_number(account_number) == "N/A"

@pytest.mark.parametrize("card_info, expected_masked_number", [
    ("Visa 1234567812345678", "Visa 1234 **** **** 5678"),
    ("MasterCard 9876543210987654", "MasterCard 9876 **** **** 7654"),
    ("", "N/A"),
    ("American Express 12345678", "N/A"),  # Номер карты слишком короткий
])
def test_mask_card_number(card_info, expected_masked_number):
    assert mask_card_number(card_info) == expected_masked_number

@pytest.mark.parametrize("date_str, expected_formatted_date", [
    ("2023-12-31T23:59:59.999", "31.12.2023"),
    ("2024-03-15T12:30:00.000", "15.03.2024"),
])
def test_format_date(date_str, expected_formatted_date):
    assert format_date(date_str) == expected_formatted_date

def test_mask_card_number_long():
    assert mask_card_number("Visa 1234 5678 1234 5678 9012") == "Visa 1234 **** **** **** 9012"
