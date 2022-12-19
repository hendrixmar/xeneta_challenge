from typing import Optional

from fastapi import APIRouter
from fastapi.params import Depends
from app.ports.service import get_ports
from app.ports.utils import validate_identifier, PortColumn
from app.ports.service import fuzzy_search_port
from app.tools.utils import formatter

router = APIRouter()


@router.get("/ports")
async def get_ports_controller(identifier: Optional[str] | None = Depends(validate_identifier)):
    return get_ports(*identifier)

@router.get("/ports/search")
async def port_search_controller(key_word: str, limit: Optional[int] = 5):
    return formatter(fuzzy_search_port(key_word, get_ports('', PortColumn.NONE), limit),
                     lambda row: {key: value for value, _, key in row})
