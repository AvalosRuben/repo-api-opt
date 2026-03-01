from fastapi import APIRouter
from .service import listar_ordenes_prestashop
from .schemas import OrdenLista

router = APIRouter()

@router.get("/", response_model=OrdenLista)
def obtener_ordenes():
    return listar_ordenes_prestashop()