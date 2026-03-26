from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session, joinedload

from app.database import engine, get_db
from fastapi import HTTPException
from app import models

from app.schemas import User
from app.schemas import Product
from app.schemas import ProductCreate
from app.schemas import ProductWithOwner
from app.schemas import CategoryCreate, Category
from app.schemas import ProductCategoryAssign  
from app.schemas import ProductWithCategories 


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
def list_products(
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
):

    products = (
        db.query(models.Product)
        .limit(limit)
        .offset(offset)
        .all()
    )

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

    products = db.query(models.Product).options(joinedload(models.Product.owner)).all()

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

@app.post("/categories", response_model=Category)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):

    new_category = models.Category(name=category.name)

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category

@app.get("/categories", response_model=list[Category])
def list_categories(db: Session = Depends(get_db)):
    categories = db.query(models.Category).all()
    return categories

@app.post("/products/{product_id}/categories")
def assign_categories_to_product(
    product_id: int,
    data: ProductCategoryAssign,
    db: Session = Depends(get_db)
):

    product = db.query(models.Product).filter(models.Product.id == product_id).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    categories = db.query(models.Category).filter(
        models.Category.id.in_(data.category_ids)
    ).all()

    if not categories:
        raise HTTPException(status_code=404, detail="Categories not found")

    product.categories.extend(categories)

    db.commit()

    return {"message": "Categories assigned to product"}


@app.get("/products/{product_id}/categories", response_model=ProductWithCategories)
def get_product_with_categories(product_id: int, db: Session = Depends(get_db)):

    product = (
        db.query(models.Product)
        .options(joinedload(models.Product.categories))
        .filter(models.Product.id == product_id)
        .first()
    )

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return product