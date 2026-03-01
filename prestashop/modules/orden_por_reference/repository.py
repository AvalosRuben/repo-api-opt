import requests
from fastapi import HTTPException
from prestashop.core.prestashop_client import BASE_URL, API_KEY  # reutilizamos config del equipo


def _ps_get_custom(endpoint: str, params: dict | None = None):
    """
    GET custom para este módulo (no toca prestashop_client.py).
    Soporta params (filtros, display, etc).
    """
    url = f"{BASE_URL}/{endpoint}"

    q = {"output_format": "JSON"}
    if params:
        q.update(params)

    try:
        response = requests.get(url, params=q, auth=(API_KEY, ""))

        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Recurso no encontrado")

        if response.status_code == 401:
            raise HTTPException(status_code=401, detail="Autenticación fallida")

        response.raise_for_status()
        return response.json()

    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="No se pudo conectar a PrestaShop")

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Tiempo de espera agotado al conectar con PrestaShop")

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def _extraer_primer_id_orden(data: dict) -> str | None:
    """
    Extrae el primer ID de orden desde la respuesta JSON.
    """
    orders = data.get("orders")
    if not orders:
        return None

    # Caso A: {"orders": [{"id": "12"}]}
    if isinstance(orders, list) and orders and isinstance(orders[0], dict):
        oid = orders[0].get("id")
        return str(oid) if oid else None

    # Caso B: {"orders": {"order": [{"id": "12"}]}}
    if isinstance(orders, dict):
        inner = orders.get("order")
        if isinstance(inner, list) and inner and isinstance(inner[0], dict):
            oid = inner[0].get("id")
            return str(oid) if oid else None
        if isinstance(inner, dict):
            oid = inner.get("id")
            return str(oid) if oid else None

    return None


def _extraer_order_payload(detalle: dict) -> dict:
    """
    Extrae el objeto 'order' real sin importar cómo venga la respuesta JSON.
    """
    order = None

    # Caso 1: {"order": {...}}
    if isinstance(detalle, dict) and isinstance(detalle.get("order"), dict):
        order = detalle["order"]

    # Caso 2: {"orders": [ {...} ]}
    elif isinstance(detalle, dict) and isinstance(detalle.get("orders"), list) and detalle["orders"]:
        first = detalle["orders"][0]
        if isinstance(first, dict):
            order = first

    # Caso 3: {"orders": {"order": [ {...} ]}} o {"orders": {"order": {...}}}
    elif isinstance(detalle, dict) and isinstance(detalle.get("orders"), dict):
        inner = detalle["orders"].get("order")
        if isinstance(inner, list) and inner and isinstance(inner[0], dict):
            order = inner[0]
        elif isinstance(inner, dict):
            order = inner

    return order if isinstance(order, dict) else {}


def obtener_orden_por_reference(reference: str):
    """
    Busca orden por reference. Si no existe, regresa None.
    """
    try:
        ref = (reference or "").strip()
        if not ref:
            return None

        # 1) Buscar ID por reference
        data_busqueda = _ps_get_custom(
            "orders",
            params={
                "filter[reference]": f"[{ref}]",
                "display": "[id,reference]",
            },
        )

        order_id = _extraer_primer_id_orden(data_busqueda)
        if not order_id:
            return None

        # 2) Traer orden completa por ID
        detalle = _ps_get_custom(
            f"orders/{order_id}",
            params={"display": "full"},
        )

        order = _extraer_order_payload(detalle)

        # Si por alguna razón no pudimos extraer la orden, tratamos de fallar “suave”
        if not order:
            return None

        # 3) Limpieza de campos (como hacen tus compas con suppliers)
        return {
            "id": int(order.get("id")) if order.get("id") else None,
            "reference": order.get("reference"),
            "id_customer": int(order.get("id_customer")) if order.get("id_customer") else None,
            "current_state": int(order.get("current_state")) if order.get("current_state") else None,
            "total_paid": float(order.get("total_paid")) if order.get("total_paid") else None,
            "date_add": order.get("date_add"),
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))