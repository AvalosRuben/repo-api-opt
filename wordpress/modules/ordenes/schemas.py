from pydantic import BaseModel

class OrdenWordpress(BaseModel):
    id: int
    status: str | None
    total: str | None
    currency: str | None
    date_created: str | None

class OrdenListaWordpress(BaseModel):
    total: int
    data: list[OrdenWordpress]