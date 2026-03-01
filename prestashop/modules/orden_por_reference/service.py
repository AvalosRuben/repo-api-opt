from .repository import obtener_orden_por_reference

def buscar_orden_por_reference(reference: str):
    orden = obtener_orden_por_reference(reference)

    if not orden:
        return {"total": 0, "data": []}

    return {"total": 1, "data": [orden]}