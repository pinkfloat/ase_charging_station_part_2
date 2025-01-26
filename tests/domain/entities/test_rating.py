# tests/domain/entities/test_rating.py
import pytest
from domain.entities.rating import Rating

# Test valid initialization
def test_rating_valid():
    # Valid rating between 1 and 5
    rating = Rating("John Doe", 3)
    assert rating.user_name == "John Doe"
    assert rating.value == 3
    assert rating.comment == ""

def test_rating_boundary_lower():
    # Test the lower boundary value (1)
    rating = Rating("Jane Doe", 1)
    assert rating.user_name == "Jane Doe"
    assert rating.value == 1
    assert rating.comment == ""

def test_rating_boundary_upper():
    # Test the upper boundary value (5)
    rating = Rating("Alice", 5)
    assert rating.user_name == "Alice"
    assert rating.value == 5
    assert rating.comment == ""

def test_rating_with_comment():
    # Test valid rating with comment
    rating = Rating("Bob", 4, "Great station!")
    assert rating.user_name == "Bob"
    assert rating.value == 4
    assert rating.comment == "Great station!"

# Test invalid rating values
def test_rating_invalid_too_low():
    # Test rating value lower than 1 (e.g., 0)
    with pytest.raises(ValueError, match="Rating must be between 1 and 5"):
        Rating("Bob", 0)

def test_rating_invalid_too_high():
    # Test rating value higher than 5 (e.g., 6)
    with pytest.raises(ValueError, match="Rating must be between 1 and 5"):
        Rating("Charlie", 6)

def test_rating_invalid_non_integer():
    # Test with a non-integer value
    with pytest.raises(ValueError, match="Rating must be an integer"):
        Rating("Dave", 3.5)  # Assuming ratings should be integers 

def test_rating_invalid_comment():
    # Test invalid comment (non-string)
    with pytest.raises(ValueError, match="Comment must be a string"):
        Rating(user_name="user123", value=3, comment=123)
