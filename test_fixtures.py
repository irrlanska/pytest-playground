import pytest

@pytest.fixture
def empty_cart():
    return []

@pytest.fixture
def cart_with_items():
    return [
        {"name": "apple", "price": 10},
        {"name": "banana", "price": 20}
    ]

def test_empty_cart_total_is_zero(empty_cart):
    total = sum(item["price"] for item in empty_cart)
    assert total == 0

def test_add_item_to_cart(empty_cart):
    empty_cart.append({"name": "orange", "price": 15})
    assert len(empty_cart) == 1
    assert empty_cart[0]["name"] == "orange"

def test_cart_total(cart_with_items):
    total = sum(item["price"] for item in cart_with_items)
    assert total == 30