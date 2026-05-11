from fastapi import FastAPI

# ODOO IMPORTS
from odoo.modules.productos.routes import router as productos_router
from odoo.modules.categorias.routes import router as categorias_router
from odoo.modules.stock.routes import router as stock_router
from odoo.modules.proveedores.routes import router as proveedores_router
from odoo.modules.ordenes.routes import router as ordenes_router

# WORDPRESS IMPORTS
from wordpress.modules.productos.routes import router as wordpress_productos_router
from wordpress.modules.ordenes.routes import router as ordenes_wp_router
from wordpress.modules.list_products.routes import router as wordpress_list_products_router
from wordpress.modules.clientes.routes import router as wordpress_clientes_router
from wordpress.modules.cupones.routes import router as wordpress_cupones_router


# PRESTASHOP IMPORTS
from prestashop.modules.clientes.routes import router as clientes_router
from prestashop.modules.productos.routes import router as prestashop_productos_router
from prestashop.modules.proveedores.routes import router as proveedores_prestashop_router
from prestashop.modules.orden_por_reference.routes import router as orden_ref_router
from prestashop.modules.pagos.routes import router as pagos_prestashop_router
from prestashop.modules.ordenes.routes import router as prestashop_ordenes_router
from prestashop.modules.productos_reference.routes import router as productos_ref_router
from prestashop.modules.ordenes_get.routes import router as ordenes_get_router  # <-- NUEVO
from prestashop.modules.actualizar_productos.routes import router as actualizar_productos_router
from prestashop.modules.desactivar_productos.routes import router as desactivar_producto_router



app = FastAPI(title="API")

# ============================================
# ODOO ENDPOINTS
# ============================================

app.include_router(productos_router, prefix="/api/odoo/productos", tags=["ODOO - Productos"])
app.include_router(categorias_router, prefix="/api/odoo/categoria", tags=["ODOO - Categorías"])
app.include_router(stock_router, prefix="/api/odoo/stock", tags=["ODOO - Stock"])
app.include_router(proveedores_router, prefix="/api/odoo/proveedores", tags=["ODOO - Proveedores"])
app.include_router(ordenes_router, prefix="/api/odoo/ordenes", tags=["ODOO - Órdenes"])

# ============================================
# PRESTASHOP ENDPOINTS
# ============================================

app.include_router(clientes_router, prefix="/api/prestashop/clientes", tags=["PrestaShop - Clientes"])
app.include_router(prestashop_productos_router, prefix="/api/prestashop/productos", tags=["PrestaShop - Productos"])
app.include_router(productos_ref_router, prefix="/api/prestashop/productos-referencia", tags=["PrestaShop - Productos Referencia"])
app.include_router(proveedores_prestashop_router, prefix="/api/prestashop/proveedores", tags=["PrestaShop - Proveedores"])
app.include_router(orden_ref_router, prefix="/api/prestashop/orden_por_reference", tags=["PrestaShop - Órdenes"])
app.include_router(pagos_prestashop_router, prefix="/api/prestashop/pagos", tags=["PrestaShop - Pagos"])
app.include_router(prestashop_ordenes_router, prefix="/api/prestashop/ordenes", tags=["PrestaShop - Órdenes"])
app.include_router(ordenes_get_router, prefix="/api/prestashop/ordenes-get", tags=["PrestaShop - Órdenes"])
app.include_router(actualizar_productos_router, prefix="/api/prestashop/actualizar-productos", tags=["PrestaShop - Productos"])
app.include_router(desactivar_producto_router, prefix="/api/prestashop/productos", tags=["PrestaShop - Productos"])

# ============================================
# WORDPRESS ENDPOINTS
# ============================================

app.include_router(wordpress_productos_router, prefix="/api/wordpress/productos", tags=["WordPress - Productos"])
app.include_router(ordenes_wp_router, prefix="/api/wordpress/ordenes", tags=["WordPress Órdenes"])
app.include_router(wordpress_list_products_router, prefix="/api/wordpress/list-products", tags=["WordPress - List Products"])

app.include_router(wordpress_clientes_router, prefix="/api/wordpress/clientes", tags=["WordPress - Clientes"]) #Endpoint Rubén
app.include_router( wordpress_clientes_router, prefix="/api/wordpress/clientes", tags=["WordPress - Clientes"])
app.include_router(wordpress_cupones_router, prefix="/api/wordpress/cupones", tags=["WordPress - Cupones"]) #Endpoint Julio
