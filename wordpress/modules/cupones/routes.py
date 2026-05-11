from fastapi import APIRouter
from .service import obtener_cupones

router = APIRouter()

@router.get("/")
def get_cupones():
    return obtener_cupones()