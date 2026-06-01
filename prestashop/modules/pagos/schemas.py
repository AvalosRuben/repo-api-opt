from pydantic import BaseModel

class Pago(BaseModel):
    id: int
    order_reference: str | None = None
    id_order: int | None = None
    amount: float
    payment_method: str | None
    date_add: str | None


class PagoLista(BaseModel):
    total: int
    data: list[Pago]