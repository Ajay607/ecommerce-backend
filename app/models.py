from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Numeric, Table, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True)

    products = relationship("Product", back_populates="owner")

product_categories = Table(
    "product_categories",
    Base.metadata,
    Column("product_id", ForeignKey("products.id"), primary_key=True),
    Column("category_id", ForeignKey("categories.id"), primary_key=True)
)
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True)

    products = relationship(
        "Product",
        secondary=product_categories,
        back_populates="categories"
    )


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Numeric, nullable=False)

    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="products")

    categories = relationship(
        "Category",
        secondary=product_categories,
        back_populates="products"
    )
    
    
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    total_amount = Column(Numeric, default=0)

    status = Column(String, default="placed")

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")

    items = relationship("OrderItem", back_populates="order")
    

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(Integer, ForeignKey("orders.id"))

    product_id = Column(Integer, ForeignKey("products.id"))

    quantity = Column(Integer, nullable=False)

    price = Column(Numeric, nullable=False)

    order = relationship("Order", back_populates="items")

    product = relationship("Product")