import pytest

def is_even(number):
 return number % 2 == 0

@pytest.mark.parametrize("number, expected", [    
    (2, True),
    (3, False),
    (0, True),
    (-2, True),
    (-3, False),
    (100, True)
])
def test_is_even(number, expected):
 assert is_even(number) == expected