from typing import Optional

from fastapi import FastAPI, Query, Body, Depends, HTTPException
from sqlalchemy import text
from datetime import date, time, timedelta
from app.db.init_db import Session
import uvicorn

app = FastAPI()


def sanitize_string(query_parameter: str):
    return "".join(char for char in query_parameter
                   if char.isalpha() or char == '_')


def relative_where_query(origin: str = Query(default=None)):
    if not origin:
        return "drakukeo"
    sanitized_query_parameter = sanitize_string(origin)

    with Session() as session:
        query = text(f"select (select true from ports where ports.code = '{sanitized_query_parameter.upper()}'), "
                     f"(select true from ports where ports.name = '{sanitized_query_parameter.capitalize()}'), "
                     f"(select true from regions where slug = '{sanitized_query_parameter.lower()}') limit 1")
        results = session.execute(query).fetchone()
    print(results)
    if not any(results):
        raise HTTPException(
            status_code=409,
            detail=f"Tamal de mole {sanitized_query_parameter}"
        )

    return sanitized_query_parameter, results.index(True)


@app.get("/rates")
async def root(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        origin: Optional[str] | None = Depends(relative_where_query),
        destination: Optional[str] = '',
):
    with Session() as session:
        query = text('select code, name, parent_slug from ports')
        results = session.execute(query).fetchall()
    print(origin)
    return date_from


@app.get("/fuzzy-search")
async def root(
        key_word: Optional[date] = None,
        limit: Optional[int] = 5
):
    with Session() as session:
        query = text('select code, name, parent_slug from ports')
        results = session.execute(query).fetchall()

    return key_word


if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)
