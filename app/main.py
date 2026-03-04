from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session, selectinload

from app.database import engine, get_db
from fastapi import HTTPException
from app import models

from app.schemas import User
from app.schemas import Product
from app.schemas import ProductCreate
from app.schemas import ProductWithOwner


# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-commerce Backend API")


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "ecommerce-backend"
    }


@app.get("/users", response_model=list[User])
def list_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@app.get("/products", response_model=list[Product])
def list_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products

@app.post("/products", response_model=Product)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):

    # Check if owner exists
    owner = db.query(models.User).filter(models.User.id == product.owner_id).first()

    if owner is None:
        raise HTTPException(status_code=404, detail="Owner not found")

    # Create Product object
    new_product = models.Product(
        name=product.name,
        price=product.price,
        owner_id=product.owner_id
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@app.get("/products-with-owner", response_model=list[ProductWithOwner])
def products_with_owner(db: Session = Depends(get_db)):

    products = db.query(models.Product).options(selectinload(models.Product.owner)).all()

    result = []

    for product in products:
        result.append({
            "product_id": product.id,
            "product_name": product.name,
            "price": float(product.price),
            "owner_name": product.owner.name,
            "owner_email": product.owner.email
        })

    return result