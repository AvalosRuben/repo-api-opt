from wordpress.core.wordpress_client import wcapi


def obtener_clientes():
    response = wcapi.get("customers")

    return response.json()