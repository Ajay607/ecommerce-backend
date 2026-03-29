from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool

    class Config:
        from_attributes = True

class Product(BaseModel):
    id: int
    name: str
    price: float
    owner_id: int

    class Config:
        from_attributes = True

class ProductCreate(BaseModel):
    name: str
    price: float
    owner_id: int

    class Config:
        from_attributes = True

class ProductWithOwner(BaseModel):
    product_id: int
    product_name: str
    price: float
    owner_name: str
    owner_email: str

    class Config:
        from_attributes = True

class CategoryCreate(BaseModel):
    name: str


class Category(BaseModel):
    id: int
    name: str
    is_active: bool

    class Config:
        from_attributes = True

class ProductCategoryAssign(BaseModel):
    category_ids: list[int]
    

class CategorySimple(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class ProductWithCategories(BaseModel):
    id: int
    name: str
    price: float
    categories: list[CategorySimple]

    class Config:
        from_attributes = True
        

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    

class OrderCreate(BaseModel):
    user_id: int
    items: list[OrderItemCreate]
    

class OrderItemResponse(BaseModel):
    product_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True
        

class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_amount: float
    status: str
    items: list[OrderItemResponse]

    class Config:
        from_attributes = True
        

class ProductSimple(BaseModel):
    id: int
    name: str
    price: float

    class Config:
        from_attributes = True
        
        
class OrderItemResponse(BaseModel):
    quantity: int
    price: float
    product: ProductSimple

    class Config:
        from_attributes = True
        

class ProductSimple(BaseModel):
    id: int
    name: str
    price: float

    class Config:
        from_attributes = True
        

class OrderItemResponse(BaseModel):
    quantity: int
    price: float
    product: ProductSimple

    class Config:
        from_attributes = True