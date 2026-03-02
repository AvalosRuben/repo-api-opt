from .repository import desactivar_producto_en_prestashop

def procesar_desactivacion(reference: str):
    resultado = desactivar_producto_en_prestashop(reference)
    return {
        "mensaje": "Producto desactivado exitosamente",
        "reference": reference,
        "prestashop_response": resultado
    }