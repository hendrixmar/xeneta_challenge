from typing import Optional, List

from fastapi import APIRouter, Query
from fastapi.params import Depends
from pydantic.datetime_parse import date

from app.rates.utils import validate_destination, validate_origin, AggregateFunctions
from app.rates.service import get_rates

router = APIRouter()


@router.get("/rates")
async def get_rates_controller(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        aggregate_functions: Optional[List[AggregateFunctions]] | None = Query(default=[AggregateFunctions.AVG]),
        origin: Optional[str] = Depends(validate_origin),
        destination: Optional[str] | None = Depends(validate_destination),
):
    return get_rates(date_from, date_to, origin, destination, aggregate_functions)
