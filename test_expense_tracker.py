import pytest
from expense_tracker import build_expense

def test_build_expense():
    result = build_expense([], 100, "food", "lunch")
    assert result[0]["amount"] == 100
    assert result[0]["id"] == 1
    assert result[0]["category"] == "food" 
    assert result[0]["description"] == "lunch"

def test_build_empty_list():
    result = build_expense([], 100, "food", "lunch")
    assert result[0]["id"] == 1

def test_build_expense_increments_id():
    existing = [{"id": 1, "amount": 50, "category": "food", "description": "coffee", "date": "2026-08-14"}]
    result = build_expense(existing, 100, "food", "lunch")
    assert result[1]["id"] == 2

def test_build_expense_negitive_amount():
    with pytest.raises(ValueError):
        build_expense([], -50, "food", "lunch")

def test_build_expense_zero_amount():
    result = build_expense([], 0, "food", "lunch")
    assert result[0]["amount"] == 0