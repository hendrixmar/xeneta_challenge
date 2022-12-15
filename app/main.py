from fastapi import FastAPI
from sqlalchemy import text

from app.db.init_db import Session
app = FastAPI()


@app.get("/")
async def root():
    with Session() as session:
        query = text('select code, name, parent_slug from ports')
        results = session.execute(query).fetchall()
        print(type(results))
    return {}


class Select:

    def __init__(self, table_name, *columns):
        self.query = f"SELECT {', '.join(columns)} from {table_name}"

    def where(self, *conditions):

        return

def select(table_name, *columns):

    return f"SELECT {', '.join(columns)} from {table_name}"

def where(*conditions):
    pass



