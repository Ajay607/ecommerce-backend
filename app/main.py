from fastapi import FastAPI
from app.database import get_db_connection
from app.schemas import User
from app.schemas import Product
from app.schemas import ProductCreate
from app.schemas import ProductWithOwner

app = FastAPI(title="E-commerce Backend API")

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "ecommerce-backend"
    }

@app.get("/users", response_model=list[User])
def list_users():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, email, is_active FROM users;")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    users = []
    for row in rows:
        users.append({
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "is_active": row[3]
        })

    return users

@app.get("/products", response_model=list[Product])
def list_products():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, price, owner_id
        FROM products;
    """)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    products = []
    for row in rows:
        products.append({
            "id": row[0],
            "name": row[1],
            "price": float(row[2]),
            "owner_id": row[3]
        })

    return products

@app.get("/products-with-owner", response_model=list[ProductWithOwner])
def products_with_owner():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            p.id,
            p.name,
            p.price,
            u.name,
            u.email
        FROM products p
        JOIN users u ON p.owner_id = u.id;
    """)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    result = []
    for row in rows:
        result.append({
            "product_id": row[0],
            "product_name": row[1],
            "price": float(row[2]),
            "owner_name": row[3],
            "owner_email": row[4]
        })

    return result


@app.post("/products", response_model=Product)
def create_product(product: ProductCreate):

    conn = get_db_connection()
    cursor = conn.cursor()

    # check owner exists
    cursor.execute(
        "SELECT id FROM users WHERE id = %s;",
        (product.owner_id,)
    )

    owner = cursor.fetchone()

    if owner is None:

        cursor.close()
        conn.close()

        return {"error": "Owner not found"}

    # insert product

    cursor.execute(
        """
        INSERT INTO products (name, price, owner_id)
        VALUES (%s, %s, %s)
        RETURNING id, name, price, owner_id;
        """,
        (product.name, product.price, product.owner_id)
    )

    new_product = cursor.fetchone()

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "id": new_product[0],
        "name": new_product[1],
        "price": float(new_product[2]),
        "owner_id": new_product[3]
    }


@app.get("/products-with-owner", response_model=list[ProductWithOwner])
def products_with_owner():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            p.id,
            p.name,
            p.price,
            u.name,
            u.email
        FROM products p
        JOIN users u ON p.owner_id = u.id;
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    result = []

    for row in rows:

        result.append({
            "product_id": row[0],
            "product_name": row[1],
            "price": float(row[2]),
            "owner_name": row[3],
            "owner_email": row[4]
        })

    return result