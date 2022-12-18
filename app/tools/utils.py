from enum import Enum
from typing import Optional, Tuple, Literal
from rapidfuzz import process, fuzz
from fastapi import FastAPI, Query, Body, Depends, HTTPException
from sqlalchemy import text
from app.db.init_db import Session
import uvicorn


def sanitize_string(query_parameter: str) -> str:
    return "".join(char for char in query_parameter if char.isalpha() or char in "_")
