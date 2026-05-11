from fastapi import APIRouter
from .service import obtener_cupones, obtener_cupon_por_id

router = APIRouter()

@router.get("/")
def get_cupones():
    return obtener_cupones()


@router.get("/{cupon_id}")
def get_cupon(cupon_id: int):
    return obtener_cupon_por_id(cupon_id)