from fastapi import APIRouter
from .service import procesar_desactivacion

router = APIRouter()

@router.patch("/{reference}/desactivar")
def desactivar_producto(reference: str):
    return procesar_desactivacion(reference)