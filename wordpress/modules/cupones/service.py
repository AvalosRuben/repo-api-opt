from fastapi import HTTPException
from wordpress.core.wordpress_client import wcapi


def obtener_cupones():
    response = wcapi.get("coupons")

    print(response.status_code)
    print(response.text)

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )

    return response.json()


def obtener_cupon_por_id(cupon_id: int):
    """Obtiene un cupón por ID. Si no existe, retorna mensaje simple."""
    try:
        response = wcapi.get(f"coupons/{cupon_id}")
    except Exception as e:
        return {"error": f"Error al conectar con WordPress: {e}"}

    if response.status_code == 404:
        return {"error": "El cupón no existe"}
    
    if response.status_code != 200:
        return {"error": f"Error: {response.text}"}

    return response.json()