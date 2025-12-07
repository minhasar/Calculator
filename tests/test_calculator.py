"""Unit tests for calculator module."""

import pytest
from calculator import add, subtract, multiply, divide


class TestAdd:
    def test_positive_numbers(self):
        assert add(2, 3) == 5

    def test_negative_numbers(self):
        assert add(-2, -3) == -5

    def test_mixed_numbers(self):
        assert add(-2, 3) == 1


class TestSubtract:
    def test_positive_numbers(self):
        assert subtract(5, 3) == 2

    def test_negative_numbers(self):
        assert subtract(-2, -3) == 1

    def test_mixed_numbers(self):
        assert subtract(3, -2) == 5


class TestMultiply:
    def test_positive_numbers(self):
        assert multiply(3, 4) == 12

    def test_negative_numbers(self):
        assert multiply(-2, -3) == 6

    def test_zero(self):
        assert multiply(5, 0) == 0


class TestDivide:
    def test_positive_numbers(self):
        assert divide(10, 2) == 5

    def test_float_result(self):
        assert divide(5, 2) == 2.5

    def test_divide_by_zero(self):
        with pytest.raises(ValueError):
            divide(5, 0)

    def test_negative_numbers(self):
        assert divide(-10, 2) == -5
