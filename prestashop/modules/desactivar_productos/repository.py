from fastapi import HTTPException
from prestashop.core.prestashop_client import prestashop_get, prestashop_put

def desactivar_producto_en_prestashop(reference: str):
    try:
        data = prestashop_get(f"products?filter[reference]=[{reference}]")
        productos = data.get("products", [])
        
        if not productos:
            raise HTTPException(status_code=404, detail=f"Producto con referencia {reference} no encontrado.")
            
        # Tomamos el producto completo
        producto_completo = productos[0]
        product_id = producto_completo.get("id")

        forbidden = [
            "manufacturer_name", "quantity", "id_default_image", 
            "position_in_category", "cache_default_attribute", 
            "id_default_combination", "associations"
        ]
        for key in forbidden:
            producto_completo.pop(key, None)

        # Cambiar el estado a inactivo
        # PrestaShop espera strings para los booleanos en su XML
        producto_completo["active"] = "0" 

        # Enviar el PUT
        payload = {"product": producto_completo}
        respuesta = prestashop_put(f"products/{product_id}", payload)
        
        return respuesta

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))