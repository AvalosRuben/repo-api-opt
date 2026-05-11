from pydantic import BaseModel, EmailStr


class AddressSchema(BaseModel):
    address_1: str
    city: str
    country: str


class ClienteCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    username: str
    password: str

    billing: AddressSchema
    shipping: AddressSchema