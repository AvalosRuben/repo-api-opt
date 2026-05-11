from fastapi import APIRouter
from .service import obtener_clientes

router = APIRouter()


@router.get("/")
def get_clientes():
    return obtener_clientes()