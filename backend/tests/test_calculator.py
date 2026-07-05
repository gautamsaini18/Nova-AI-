"""Tests for Calculator Service."""

import pytest
from backend.modules.calculator.service import CalculatorService, Operation


class TestCalculatorService:
    def test_add(self):
        assert CalculatorService.calculate(Operation.ADD, 5, 3) == 8

    def test_subtract(self):
        assert CalculatorService.calculate(Operation.SUBTRACT, 10, 4) == 6

    def test_multiply(self):
        assert CalculatorService.calculate(Operation.MULTIPLY, 6, 7) == 42

    def test_divide(self):
        assert CalculatorService.calculate(Operation.DIVIDE, 15, 3) == 5

    def test_divide_by_zero(self):
        with pytest.raises(ValueError, match="Division by zero"):
            CalculatorService.calculate(Operation.DIVIDE, 10, 0)

    def test_power(self):
        assert CalculatorService.calculate(Operation.POWER, 2, 10) == 1024

    def test_sqrt(self):
        assert CalculatorService.calculate(Operation.SQRT, 144) == 12

    def test_sqrt_negative(self):
        with pytest.raises(ValueError, match="negative"):
            CalculatorService.calculate(Operation.SQRT, -1)

    def test_percent(self):
        assert CalculatorService.calculate(Operation.PERCENT, 25, 200) == 50

    def test_sin(self):
        assert abs(CalculatorService.calculate(Operation.SIN, 90) - 1) < 0.001

    def test_cos(self):
        assert abs(CalculatorService.calculate(Operation.COS, 0) - 1) < 0.001

    def test_tan(self):
        assert abs(CalculatorService.calculate(Operation.TAN, 45) - 1) < 0.001

    def test_log(self):
        assert abs(CalculatorService.calculate(Operation.LOG, 100) - 2) < 0.001

    def test_ln(self):
        assert abs(CalculatorService.calculate(Operation.LN, 2.71828) - 1) < 0.01

    def test_abs(self):
        assert CalculatorService.calculate(Operation.ABS, -42) == 42

    def test_round(self):
        assert CalculatorService.calculate(Operation.ROUND, 3.14159, 2) == 3.14

    def test_floor(self):
        assert CalculatorService.calculate(Operation.FLOOR, 3.9) == 3

    def test_ceil(self):
        assert CalculatorService.calculate(Operation.CEIL, 3.1) == 4

    def test_evaluate_expression(self):
        assert CalculatorService.evaluate_expression("2 + 3 * 4") == 14

    def test_evaluate_with_power(self):
        assert CalculatorService.evaluate_expression("2 ^ 10") == 1024

    def test_evaluate_invalid(self):
        with pytest.raises(ValueError):
            CalculatorService.evaluate_expression("invalid + +")

    def test_format_result_integer(self):
        assert CalculatorService.format_result(42.0) == "42"

    def test_format_result_decimal(self):
        assert CalculatorService.format_result(3.14159) == "3.1416"

    def test_format_result_nan(self):
        assert CalculatorService.format_result(float("nan")) == "NaN"

    def test_format_result_inf(self):
        assert CalculatorService.format_result(float("inf")) == "Infinity"
