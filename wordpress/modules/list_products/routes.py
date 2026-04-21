from fastapi import APIRouter
from .service import obtener_productos_wordpress
from .schemas import ProductoListaWordpress

router = APIRouter()


@router.get("/", response_model=ProductoListaWordpress)
def listar_productos():
    return obtener_productos_wordpress()
