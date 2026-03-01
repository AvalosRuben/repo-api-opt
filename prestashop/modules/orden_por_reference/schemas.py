from pydantic import BaseModel

class Orden(BaseModel):
    id: int | None
    reference: str | None
    id_customer: int | None
    current_state: int | None
    total_paid: float | None
    date_add: str | None

class OrdenLista(BaseModel):
    total: int
    data: list[Orden]