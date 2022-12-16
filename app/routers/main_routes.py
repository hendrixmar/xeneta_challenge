from typing import Optional

from fastapi import APIRouter
from fastapi.params import Depends
from pydantic.datetime_parse import date
from sqlalchemy import text

from app.db.init_db import Session
from app.tools.validation import validate_destination, validate_origin

router = APIRouter()


@router.get("/fuzzy-search")
async def root(
    key_word: Optional[date] = None,
    limit: Optional[int] = 5
):
    with Session() as session:
        query = text('select code, name, parent_slug from ports')
        results = session.execute(query).fetchall()

    return key_word

@router.get("/rates")
async def root(
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    origin: Optional[str] = Depends(validate_origin),
    destination: Optional[str] | None = Depends(validate_destination),
):
    with Session() as session:
        query = text('select code, name, parent_slug from ports')
        results = session.execute(query).fetchall()
    print(origin, destination, date_to, date_from)
    return date_from