from woocommerce import API

# Configuración de la conexión
wcapi = API(
    url="http://localhost:8081", # Asegúrate de que el puerto sea el correcto (8080)
    
    # IMPORTANTE COLOCAR SUS PROPIAS CREDENCIALES PARA PODER CONECTARSE AL WORDPRESS
    consumer_key="ck_5c02e688fac26112bce3f033cbf8129a87b36506",
    consumer_secret="cs_d00898ad67c2e30eaae3d40efd4eae7118d481e9",
    version="wc/v3",
    timeout=20
)