# tests/domain/value_objects/test_postal_code.py
import pytest
from domain.value_objects.postal_code import PostalCode

# Test successful initialization with a string
def test_postal_code_valid():
    postal_code = PostalCode("12345")
    assert postal_code.plz == "12345"

# Test successful initialization with an int
def test_postal_code_int():
    postal_code = PostalCode(12345)
    assert postal_code.plz == "12345"

# Test invalid postal code: too short
def test_postal_code_invalid_too_short():
    with pytest.raises(ValueError, match="Invalid postal code"):
        PostalCode("123")

# Test invalid postal code: too long
def test_postal_code_invalid_too_long():
    with pytest.raises(ValueError, match="Invalid postal code"):
        PostalCode("123456")

# Test invalid postal code: contains non-digit characters
def test_postal_code_invalid_non_digits():
    with pytest.raises(ValueError, match="Invalid postal code"):
        PostalCode("12A45")

# Test empty string
def test_postal_code_empty():
    with pytest.raises(ValueError, match="Invalid postal code"):
        PostalCode("")
