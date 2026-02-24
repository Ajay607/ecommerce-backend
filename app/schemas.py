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