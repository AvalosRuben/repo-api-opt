from fastapi import HTTPException
from wordpress.core.wordpress_client import wcapi


def obtener_cupon_por_id(cupon_id: int):
    response = wcapi.get(f"coupons/{cupon_id}")

    print(response.status_code)
    print("No existe ese cupon" if response.status_code == 404 else response.text)

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )

    return response.json()
