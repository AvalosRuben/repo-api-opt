from fastapi import HTTPException
from wordpress.core.wordpress_client import wcapi

def obtener_ordenes_wordpress():
    try:
        # El cliente wcapi ya sabe cómo construir la URL, solo le pasamos el recurso "orders"
        response = wcapi.get("orders")
        
        # Validamos si hubo un error del lado de WooCommerce (ej. credenciales inválidas)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, 
                detail=f"Error de WooCommerce: {response.text}"
            )
        
        ordenes = response.json()
        
        # Mapeamos los datos para que coincidan exactamente con nuestro Schema
        resultado = []
        for orden in ordenes:
            resultado.append({
                "id": orden.get("id"),
                "status": orden.get("status"),
                "total": orden.get("total"),
                "currency": orden.get("currency"),
                "date_created": orden.get("date_created")
            })
            
        return {"total": len(resultado), "data": resultado}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))