from fastapi import FastAPI
from database import engine

app = FastAPI(
    title="Online Pharmacy Ordering Platform",
    description="Backend API for online pharmacy ordering system",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Online Pharmacy API is running!"
    }


@app.get("/health")
def health_check():
    try:
        with engine.connect():
            return {
                "status": "healthy",
                "database": "connected"
            }
    except Exception:
        return {
            "status": "unhealthy",
            "database": "disconnected"
        }