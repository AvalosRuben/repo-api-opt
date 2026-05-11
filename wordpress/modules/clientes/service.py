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


def obtener_cliente_por_id(cliente_id: int):
    try:
        response = wcapi.get(f"customers/{cliente_id}")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error connecting to WordPress: {e}")

    # Debug prints (visible in uvicorn terminal)
    print("[WP] GET customers/{id} ->", cliente_id)
    print("[WP] status:", response.status_code)
    print("[WP] text:", response.text)

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )

    return response.json()