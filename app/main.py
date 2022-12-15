from typing import Optional

from fastapi import FastAPI, Query, Body
from sqlalchemy import text
from datetime import date, time, timedelta
from app.db.init_db import Session
import uvicorn

app = FastAPI()


@app.get("/rates")
async def root(
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    origin: Optional[str] = '',
    destination: Optional[str] = '',
):
    with Session() as session:
        query = text('select code, name, parent_slug from ports')
        results = session.execute(query).fetchall()

    return date_from


@app.get("/fuzzy-search")
async def root(
        key_word: Optional[date] = None,
):
    with Session() as session:
        query = text('select code, name, parent_slug from ports')
        results = session.execute(query).fetchall()

    return key_word


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


