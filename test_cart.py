import pytest
import time


def add_item(cart, new_item, max_size = 50):
    if len(cart) >= max_size: 
        return False
    for item in cart:
        if item["name"] == new_item["name"]:
            item["quantity"] += new_item.get("quantity", 1)
            return
    cart.append(new_item.copy())
    return True

# === Базовые операции ===

@pytest.mark.cart
@pytest.mark.fast
def test_empty_cart_total_is_zero(empty_cart):
    total = sum(item["price"] * item["quantity"] for item in empty_cart)
    assert total == 0

@pytest.mark.cart
@pytest.mark.fast
def test_add_item_increases_cart_length(empty_cart):
    add_item(empty_cart, {"name": "apple", "price": 10, "quantity": 1})
    assert len(empty_cart) == 1

@pytest.mark.cart
@pytest.mark.fast
def test_cart_total_is_sum_of_item_prices(cart_with_items):
    total = sum(item["price"] * item["quantity"] for item in cart_with_items)
    assert total == 30

@pytest.mark.cart
@pytest.mark.fast
def test_remove_item_decreases_total(cart_with_items):
    cart_with_items.pop(0)
    total = sum(item["price"] * item["quantity"] for item in cart_with_items)
    assert total == 20

@pytest.mark.cart
@pytest.mark.fast
def test_clear_cart_sets_total_to_zero(cart_with_items):
    cart_with_items.clear()
    total = sum(item["price"] * item["quantity"] for item in cart_with_items)
    assert total == 0

# === Количество ===

@pytest.mark.cart
@pytest.mark.fast
def test_zero_quantity_sets_total_to_zero(single_apple):
    single_apple[0]['quantity'] = 0
    total = sum(item["price"] * item["quantity"] for item in single_apple)
    assert total == 0

# для негативных сценариев используем raises
@pytest.mark.cart
@pytest.mark.fast
def test_negative_quantity_raises_value_error(single_apple):
    single_apple[0]["quantity"] = -1
    with pytest.raises(ValueError):
        if any (item["quantity"] < 0 for item in single_apple):
            raise ValueError('quantity must be positive')

@pytest.mark.cart
@pytest.mark.fast        
def test_fractional_quantity_calculates_correctly(fractional_cart):
    total = sum(item['price'] * item['quantity'] for item in fractional_cart)
    assert total == 30

# === Дубликаты и повторы ===

@pytest.mark.cart
@pytest.mark.fast
def test_adding_same_item_increases_quantity(single_apple):
    add_item(single_apple, {"name": "apple", "price": 10, "quantity": 1})
    assert len(single_apple) == 1
    assert single_apple[0]["quantity"] == 2
    total = sum(item["price"] * item["quantity"] for item in single_apple)
    assert total == 20    

# === Производительность ===

@pytest.mark.cart
@pytest.mark.slow
def test_performance_hundred_thousand_items(huge_cart):
    start = time.perf_counter()
    total = sum(item["price"] * item["quantity"] for item in huge_cart)
    elapsed = time.perf_counter() - start
    assert total == 1000000
    assert elapsed < 0.1, f'Слишком долго: {elapsed:.4f} s' 

# === Границы ===

@pytest.mark.cart
@pytest.mark.fast
def test_cart_exeeding_max_size_is_rejected(max_cart):
    result = add_item(max_cart, {"name": "apple", "price": 10, "quantity": 1})
    assert result is False
    assert len(max_cart) == 50

