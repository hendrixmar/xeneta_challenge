from typing import List

from sqlalchemy import text

from app.database import Session
from app.rates.utils import PortColumn


def get_ports(port_value: str, port_column: PortColumn) -> List[dict[str, str]]:
    temp_query = "select code, name, parent_slug from ports {filter}".format(
        filter=f"where {port_column.name} = '{port_value}'"
    )

    with Session() as session:
        ports_rows = session.execute(text(temp_query)).fetchall()

    return [dict(row) for row in ports_rows]
