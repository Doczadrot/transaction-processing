import json
import pytest
from main import mask_card_number, mask_account_number, format_date, get_digits, clean_up_digits

# Тесты для функции mask_account_number

@pytest.mark.parametrize("account_number, expected", [
    ("Invalid Account Number", "N/A"),  # Некорректный номер счета
    ("1234", "N/A"),  # Слишком короткий номер счета
    ("12345", "*2345"),  # Корректный номер счета
    ("Account 12345", "Account *2345"),  # Корректный номер счета с префиксом
    ("123456789987654321", "**************4321"),  # Длинный корректный номер счета
])
def test_mask_account_number_invalid_format(account_number, expected):
    assert mask_account_number(account_number) == expected

# Тесты для функции mask_card_number

@pytest.mark.parametrize("card_info, expected_masked_number", [
    ("Visa 1234567812345678", "Visa 1234 56** **** 5678"),  # Корректная Visa карта
    ("MasterCard 9876543210987654", "MasterCard 9876 54** **** 7654"),  # Корректная MasterCard карта
    ("", "N/A"),  # Пустая строка
    ("American Express 12345678", "N/A"),  # Неизвестный тип карты
])
def test_mask_card_number(card_info, expected_masked_number):
    assert mask_card_number(card_info) == expected_masked_number

# Тесты для функции format_date

@pytest.mark.parametrize("date_str, expected_formatted_date", [
    ("2023-12-31T23:59:59.999", "31.12.2023"),  # Корректная дата и время
    ("2024-03-15T12:30:00.000", "15.03.2024"),  # Корректная дата и время
])
def test_format_date(date_str, expected_formatted_date):
    assert format_date(date_str) == expected_formatted_date

# Тесты для функции get_digits

@pytest.mark.parametrize("info, expected_info", [
    ("", ""),  # Пустая строка
    ("abc", ""),  # Строка только с буквами
    ("a1b", "1"),  # Строка с буквами и цифрами
    ("123", "123"),  # Строка только с цифрами
    ("123 456", "123456"),  # Строка с пробелами
    ("123 a1b 456", "1231456"),  # Строка с буквами, цифрами и пробелами
])
def test_get_digits(info, expected_info):
    assert get_digits(info) == expected_info

# Тесты для функции clean_up_digits

@pytest.mark.parametrize("info, expected_info", [
    ("", ""),  # Пустая строка
    ("124", ""),  # Строка только с цифрами
    ("1a4", "a"),  # Строка с буквами и цифрами
    ("abc", "abc"),  # Строка только с буквами
    ("abc def", "abc def"),  # Строка с буквами и пробелами
])
def test_clean_up_digits(info, expected_info):
    assert clean_up_digits(info) == expected_info
