from fastapi import APIRouter
from .service import sincronizar_productos_odoo_a_wordpress
from .schemas import RespuestaSincronizacion, RespuestaOrdenes

router = APIRouter()

@router.post("/sincronizar-odoo", response_model=RespuestaSincronizacion)
def sincronizar_productos_desde_odoo():
    return sincronizar_productos_odoo_a_wordpress()

@router.post("/sincronizar-ordenes", response_model=RespuestaOrdenes)
def sincronizar_ordenes():
    from odoo.modules.ordenes.service import obtener_ordenes
    ordenes = obtener_ordenes()["data"]
    return enviar_ordenes_a_wordpress(ordenes)
