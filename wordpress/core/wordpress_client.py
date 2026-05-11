import os
from woocommerce import API

# Configuración de la conexión: lee valores desde variables de entorno
# Variables disponibles: WP_URL, WP_CONSUMER_KEY, WP_CONSUMER_SECRET
WC_URL = os.getenv("WP_URL", "http://localhost:8080")
WC_CONSUMER_KEY = os.getenv("WP_CONSUMER_KEY", "ck_9ed5ab647702547579f12c8bbbb49dd7b0d17064")
WC_CONSUMER_SECRET = os.getenv("WP_CONSUMER_SECRET", "cs_21b396f0cd15e6b86207a65092aa5db983c42626")

wcapi = API(
    url=WC_URL,
    consumer_key=WC_CONSUMER_KEY,
    consumer_secret=WC_CONSUMER_SECRET,
    version="wc/v3",
    timeout=20
)