from fastapi import APIRouter

from .schemas import ClienteCreate
from .service import obtener_clientes, crear_cliente, obtener_cliente_por_id

router = APIRouter()


@router.get("/")
def get_clientes():
    return obtener_clientes()


@router.post("/")
def post_cliente(cliente: ClienteCreate):
    return crear_cliente(cliente.model_dump())


@router.get("/{cliente_id}")
def get_cliente(cliente_id: int):
    return obtener_cliente_por_id(cliente_id)