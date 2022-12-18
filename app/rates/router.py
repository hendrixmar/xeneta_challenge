from typing import Optional, List

from fastapi import APIRouter, Query
from fastapi.params import Depends
from pydantic.datetime_parse import date
from sqlalchemy import text

from app.db.init_db import Session
from app.rates.utils import validate_destination, validate_origin, AggregateFunctions
from app.rates.service import fuzzy_search_port, formatter, get_rates

router = APIRouter()


@router.get("/rates/search")
async def root(key_word: str, limit: Optional[int] = 5):
    with Session() as session:
        query = text("select code, name, parent_slug from ports")
        ports_rows = session.execute(query).fetchall()

    return list(
        formatter(
            fuzzy_search_port(key_word, ports_rows, limit),
            lambda row: {key: value for value, _, key in row},
        )
    )


@router.get("/rates")
async def root(
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    aggregate_functions: Optional[List[AggregateFunctions]] | None = Query(default=[AggregateFunctions.AVG]),
    origin: Optional[str] = Depends(validate_origin),
    destination: Optional[str] | None = Depends(validate_destination),

):
    return get_rates(date_from, date_to, origin, destination, aggregate_functions)
