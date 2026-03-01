from fastapi import APIRouter
from .service import buscar_orden_por_reference
from .schemas import OrdenLista

router = APIRouter()

@router.get("/{reference}", response_model=OrdenLista)
def obtener_orden(reference: str):
    return buscar_orden_por_reference(reference)