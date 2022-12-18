from enum import Enum
from typing import Optional, Tuple, Literal
from rapidfuzz import process, fuzz
from fastapi import FastAPI, Query, Body, Depends, HTTPException
from sqlalchemy import text
from app.db.init_db import Session
import uvicorn

from app.tools.utils import sanitize_string
from ports.utils import check_location_existing, PortColumn


class AggregateFunctions(Enum):
    AVG = 'AVG'
    SUM = 'SUM'
    COUNT = 'COUNT'
    MAX = 'MAX'
    MIN = 'MIN'
    STD = 'STD'


def validate_origin(origin: str = Query(default=None)) -> tuple[str, PortColumn]:
    if not origin:
        return "", PortColumn.NONE

    sanitized_string = sanitize_string(origin)
    return check_location_existing(sanitized_string)


def validate_destination(
        destination: str = Query(default=None),
) -> tuple[str, PortColumn]:
    if not destination:
        return "", PortColumn.NONE

    sanitized_string = sanitize_string(destination)
    return check_location_existing(sanitized_string)
