"""Nova AI — Calculator API Router"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from backend.core.logging_config import NovaLogger
from backend.models.schemas import (
    CalculateRequest, CalculateResponse, EvaluateRequest,
)
from backend.modules.calculator.service import CalculatorService, Operation

logger = NovaLogger("api.calculator")
router = APIRouter()


@router.post("/calculate", response_model=CalculateResponse)
async def calculate(body: CalculateRequest):
    """Perform a mathematical operation."""
    try:
        operation = Operation(body.operation)
        value = CalculatorService.calculate(operation, body.a, body.b)
        formatted = CalculatorService.format_result(value)
        return CalculateResponse(
            result=formatted,
            value=value,
            operation=body.operation,
            formatted=formatted,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/evaluate", response_model=CalculateResponse)
async def evaluate(body: EvaluateRequest):
    """Evaluate a math expression string."""
    try:
        value = CalculatorService.evaluate_expression(body.expression)
        formatted = CalculatorService.format_result(value)
        return CalculateResponse(
            result=formatted,
            value=value,
            operation="evaluate",
            formatted=formatted,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
