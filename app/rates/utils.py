from enum import Enum
from typing import Optional, Tuple, Literal
from rapidfuzz import process, fuzz
from fastapi import FastAPI, Query, Body, Depends, HTTPException
from sqlalchemy import text
from app.db.init_db import Session
import uvicorn

from app.tools.utils import sanitize_string


class PortColumn(Enum):
    CODE = 1
    NAME = 2
    PARENT_SLUG = 3
    NONE = 4


def check_location_existing(location: str) -> tuple[str, PortColumn]:
    """

    Parameters:
                location (str): Code, name, or region of any port

    Returns:
            best_results (list[List[dict]]): The n number
    """
    # The query below is to match any port by their name, code, or parent_slug.
    # It will return a tuple of 3 elements. Each element represent the column that match.
    # first position: is true that means it is a correct port code
    # second position: is true that means it is a correct port name
    # third position: is true that means it is a correct slug

    with Session() as session:
        query = text(
            f"select (select true from ports where ports.code = '{location.upper()}'), "
            f"(select true from ports where ports.name = '{location.capitalize()}'), "
            f"(select true from regions where slug = '{location.lower()}') limit 1"
        )
        results = session.execute(query).fetchone()

    # In case any of the positions is true it will raise an exception
    if not any(results):
        raise HTTPException(
            status_code=404,
            detail=f"The parameter {location} isn't related with any port",
        )

    # This is done to o
    index = results.index(True)

    return location, PortColumn(index)


def validate_origin(origin: str = Query(default=None)) -> tuple[str, PortColumn]:
    if not origin:
        return '', PortColumn.NONE

    sanitized_string = sanitize_string(origin)
    return check_location_existing(sanitized_string)


def validate_destination(destination: str = Query(default=None)) -> tuple[str, PortColumn]:
    if not destination:
        return '', PortColumn.NONE

    sanitized_string = sanitize_string(destination)
    return check_location_existing(sanitized_string)