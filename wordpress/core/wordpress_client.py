from woocommerce import API

# Configuración de la conexión
wcapi = API(
    url="http://localhost:8080", # Asegúrate de que el puerto sea el correcto (8080)
    
    # IMPORTANTE COLOCAR SUS PROPIAS CREDENCIALES PARA PODER CONECTARSE AL WORDPRESS
    consumer_key="ck_b32a330f9c4dcaa3371a2002e90ec4e7f241abeb",
    consumer_secret="cs_4ba00d33766ca95fa343f5c418739ae6591545bd",
    version="wc/v3",
    timeout=20
)