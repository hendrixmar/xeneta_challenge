from typing import Optional

from fastapi import APIRouter
from fastapi.params import Depends

from app.ports.service import get_ports
from app.ports.utils import validate_identifier

router = APIRouter()


@router.get("/ports")
async def root(identifier: Optional[str] | None = Depends(validate_identifier)):
    return get_ports(*identifier)
