from fastapi import FastAPI

app = FastAPI(title="E-commerce Backend API")


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "ecommerce-backend"
    }
