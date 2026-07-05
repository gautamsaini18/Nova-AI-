"""Nova AI — Calculator Service"""

from __future__ import annotations

import math
import re
from enum import Enum
from typing import Any


class Operation(str, Enum):
    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"
    POWER = "power"
    SQRT = "sqrt"
    PERCENT = "percent"
    SIN = "sin"
    COS = "cos"
    TAN = "tan"
    LOG = "log"
    LN = "ln"
    ABS = "abs"
    ROUND = "round"
    FLOOR = "floor"
    CEIL = "ceil"


class CalculatorService:
    """Performs arithmetic and scientific calculations."""

    @staticmethod
    def calculate(operation: Operation, a: float, b: float | None = None) -> float:
        match operation:
            case Operation.ADD:
                return a + (b or 0)
            case Operation.SUBTRACT:
                return a - (b or 0)
            case Operation.MULTIPLY:
                return a * (b or 1)
            case Operation.DIVIDE:
                if b is None or b == 0:
                    raise ValueError("Division by zero")
                return a / b
            case Operation.POWER:
                return a ** (b or 2)
            case Operation.SQRT:
                if a < 0:
                    raise ValueError("Cannot take square root of negative number")
                return math.sqrt(a)
            case Operation.PERCENT:
                return a / 100 * (b or 1)
            case Operation.SIN:
                return math.sin(math.radians(a))
            case Operation.COS:
                return math.cos(math.radians(a))
            case Operation.TAN:
                if a % 180 == 90:
                    raise ValueError("Tan undefined at 90 degrees")
                return math.tan(math.radians(a))
            case Operation.LOG:
                b = b or 10
                if a <= 0:
                    raise ValueError("Log argument must be positive")
                return math.log(a, b)
            case Operation.LN:
                if a <= 0:
                    raise ValueError("Natural log argument must be positive")
                return math.log(a)
            case Operation.ABS:
                return abs(a)
            case Operation.ROUND:
                return round(a, int(b or 0))
            case Operation.FLOOR:
                return math.floor(a)
            case Operation.CEIL:
                return math.ceil(a)

    @staticmethod
    def evaluate_expression(expression: str) -> float:
        """Evaluate a math expression string safely using a restricted env."""
        cleaned = re.sub(r"[^0-9+\-*/().,%^ ]", "", expression)
        cleaned = cleaned.replace("^", "**")
        allowed = {
            "abs": abs, "round": round, "min": min, "max": max,
            "sum": sum, "pow": pow, "float": float, "int": int,
            "math": math,
        }
        try:
            result = eval(cleaned, {"__builtins__": {}}, allowed)
            return float(result)
        except Exception as e:
            raise ValueError(f"Invalid expression: {e}")

    @staticmethod
    def format_result(value: float) -> str:
        if value == float("inf") or value == float("-inf"):
            return "Infinity"
        if value != value:
            return "NaN"
        if value == int(value):
            return str(int(value))
        return f"{value:,.4f}".rstrip("0").rstrip(".")
