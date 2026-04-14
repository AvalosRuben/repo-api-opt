import requests
from fastapi import HTTPException
from wordpress.core.wordpress_client import wcapi
from odoo.core.odoo import get_odoo_connection, ODOO_DB, ODOO_PASSWORD
from .schemas import ProductoSincronizado, RespuestaSincronizacion


def obtener_productos_odoo():
    try:
        uid, models = get_odoo_connection()
        
        productos = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            "product.product", "search_read",
            [[]],
            {
                "fields": ["id", "name", "default_code", "list_price", "type", "categ_id"],
                "order": "name"
            }
        )
        
        # Normalizar datos
        for prod in productos:
            dc = prod.get("default_code")
            if dc is False:
                prod["default_code"] = None
            elif dc is not None and not isinstance(dc, str):
                prod["default_code"] = str(dc)
        
        return productos
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al conectar con ODOO: {str(e)}")


def sincronizar_productos_odoo_a_wordpress():
    try:
        # Obtener productos de ODOO
        productos_odoo = obtener_productos_odoo()
        
        detalles = []
        total_sincronizado = 0
        total_errores = 0
        
        for producto in productos_odoo:
            try:
                # Preparar datos para WooCommerce
                datos_producto = {
                    "name": producto.get("name", "Producto sin nombre"),
                    "type": "simple",  # Tipo de producto simple
                    "sku": producto.get("default_code") or f"ODOO-{producto.get('id')}",
                    "regular_price": str(producto.get("list_price", 0)) if producto.get("list_price") else "0",
                    "description": f"Producto importado de ODOO (ID: {producto.get('id')})",
                    "meta_data": [
                        {
                            "key": "odoo_id",
                            "value": str(producto.get("id"))
                        }
                    ]
                }
                
                # Buscar si el producto ya existe en WooCommerce por SKU
                try:
                    productos_existentes = wcapi.get("products", params={"sku": datos_producto["sku"]}).json()
                    
                    if productos_existentes.get("data") and len(productos_existentes.get("data", [])) > 0:
                        # Actualizar producto existente
                        producto_wc = productos_existentes["data"][0]
                        respuesta = wcapi.put(f"products/{producto_wc['id']}", datos_producto)
                    else:
                        # Crear nuevo producto
                        respuesta = wcapi.post("products", datos_producto)
                
                except Exception as e:
                    # Si hay error buscando, intentar crear uno nuevo
                    respuesta = wcapi.post("products", datos_producto)
                
                # Verificar que la solicitud fue exitosa
                if respuesta.status_code in [200, 201]:
                    total_sincronizado += 1
                    detalles.append(
                        ProductoSincronizado(
                            id_odoo=producto.get("id"),
                            nombre=producto.get("name"),
                            sku=datos_producto["sku"],
                            precio=producto.get("list_price"),
                            sincronizado=True,
                            mensaje="Producto sincronizado correctamente"
                        )
                    )
                else:
                    total_errores += 1
                    detalles.append(
                        ProductoSincronizado(
                            id_odoo=producto.get("id"),
                            nombre=producto.get("name"),
                            sku=datos_producto["sku"],
                            precio=producto.get("list_price"),
                            sincronizado=False,
                            mensaje=f"Error en WooCommerce: {respuesta.status_code}"
                        )
                    )
            
            except Exception as e:
                total_errores += 1
                detalles.append(
                    ProductoSincronizado(
                        id_odoo=producto.get("id"),
                        nombre=producto.get("name", "Sin nombre"),
                        sku=producto.get("default_code"),
                        precio=producto.get("list_price"),
                        sincronizado=False,
                        mensaje=f"Error al procesar: {str(e)}"
                    )
                )
        
        return RespuestaSincronizacion(
            total_procesados=len(productos_odoo),
            total_sincronizado=total_sincronizado,
            total_errores=total_errores,
            detalles=detalles
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en la sincronización: {str(e)}"
        )
