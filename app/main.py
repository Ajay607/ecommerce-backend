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
