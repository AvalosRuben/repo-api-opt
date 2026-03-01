from .repository import obtener_ordenes_prestashop

def listar_ordenes_prestashop():
    ordenes = obtener_ordenes_prestashop()
    return {"total": len(ordenes), "data": ordenes}