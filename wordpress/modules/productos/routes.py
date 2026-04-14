from fastapi import APIRouter
from .service import sincronizar_productos_odoo_a_wordpress
from .schemas import RespuestaSincronizacion

router = APIRouter()

@router.post("/sincronizar-odoo", response_model=RespuestaSincronizacion)
def sincronizar_productos_desde_odoo():
    return sincronizar_productos_odoo_a_wordpress()
