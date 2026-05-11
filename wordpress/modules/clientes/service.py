from fastapi import HTTPException
from wordpress.core.wordpress_client import wcapi


def obtener_clientes():
    response = wcapi.get("customers")

    print(response.status_code)
    print(response.text)

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )

    return response.json()

def crear_cliente(data):
    response = wcapi.post("customers", data)

    if response.status_code not in [200, 201]:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json()
        )

    return response.json()