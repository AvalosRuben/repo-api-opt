from prestashop.core.prestashop_client import prestashop_get
from fastapi import HTTPException


def obtener_ordenes_prestashop():
    try:
        data = prestashop_get("orders")

        orders = data.get("orders", [])
        if isinstance(orders, dict):
            orders = orders.get("order", [])

        if not isinstance(orders, list):
            orders = []

        resultado = []
        for o in orders:
            if not isinstance(o, dict):
                continue

            resultado.append({
                "id": int(o.get("id")) if o.get("id") else None,
                "reference": o.get("reference"),
                "id_customer": int(o.get("id_customer")) if o.get("id_customer") else None,
                "current_state": int(o.get("current_state")) if o.get("current_state") else None,
                "total_paid": float(o.get("total_paid")) if o.get("total_paid") else None,
                "date_add": o.get("date_add"),
            })

        return resultado

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))