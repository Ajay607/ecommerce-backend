from fastapi import FastAPI
from app.database import get_db_connection

app = FastAPI(title="E-commerce Backend API")


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "ecommerce-backend"
    }



@app.get("/users")
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

@app.get("/products")
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

@app.get("/products-with-owner")
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

