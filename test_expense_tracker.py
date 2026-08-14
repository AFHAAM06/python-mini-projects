from expense_tracker import build_expense

def test_build_expense():
    result = build_expense([], 100, "food", "lunch")
    assert result[0]["amount"] == 100
    assert result[0]["id"] == 1
    assert result[0]["category"] == "food" 
    assert result[0]["description"] == "lunch"