from pydantic import BaseModel
from typing import Optional

class ProductoOdoo(BaseModel):
    id: int
    name: str
    default_code: Optional[str] = None
    list_price: Optional[float] = None
    type: Optional[str] = None
    categ_id: Optional[list] = None

class ProductoSincronizado(BaseModel):
    id_odoo: int
    nombre: str
    sku: Optional[str] = None
    precio: Optional[float] = None
    sincronizado: bool
    mensaje: Optional[str] = None

class RespuestaSincronizacion(BaseModel):
    total_procesados: int
    total_sincronizado: int
    total_errores: int
    detalles: list[ProductoSincronizado]
