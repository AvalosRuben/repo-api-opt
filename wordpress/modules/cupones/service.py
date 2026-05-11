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