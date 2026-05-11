from fastapi import APIRouter
from .service import obtener_cupon_por_id

router = APIRouter()


@router.get("/{id}")
def get_cupon(id: int):
    return obtener_cupon_por_id(id)
