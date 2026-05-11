from fastapi import APIRouter

from .schemas import ClienteCreate
from .service import obtener_clientes, crear_cliente

router = APIRouter()


@router.get("/")
def get_clientes():
    return obtener_clientes()


@router.post("/")
def post_cliente(cliente: ClienteCreate):
    return crear_cliente(cliente.model_dump())