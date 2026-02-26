from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool

class Product(BaseModel):
    id: int
    name: str
    price: float
    owner_id: int

class ProductCreate(BaseModel):
    name: str
    price: float
    owner_id: int

class ProductWithOwner(BaseModel):
    product_id: int
    product_name: str
    price: float
    owner_name: str
    owner_email: str