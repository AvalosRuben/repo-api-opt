from pydantic import BaseModel


class ProductoWordpress(BaseModel):
    id: int
    name: str | None
    sku: str | None
    price: str | None
    status: str | None


class ProductoListaWordpress(BaseModel):
    total: int
    data: list[ProductoWordpress]
