from fastapi import APIRouter
from .service import obtener_ordenes_wordpress
from .schemas import OrdenListaWordpress

router = APIRouter()

@router.get("/", response_model=OrdenListaWordpress)
def listar_ordenes():
    return obtener_ordenes_wordpress()