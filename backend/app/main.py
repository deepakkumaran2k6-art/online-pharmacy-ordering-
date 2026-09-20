from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.medicine import router as medicine_router
from app.api.category import router as category_router
from app.api.order import router as order_router
from app.api.prescription import router as prescription_router

from app.core.database import Base, engine

from app.models.user import User
from app.models.medicine import Medicine
from app.models.category import Category
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.prescription import Prescription


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Online Pharmacy Ordering API",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(medicine_router)
app.include_router(category_router)
app.include_router(order_router)
app.include_router(prescription_router)


@app.get("/")
def root():
    return {
        "message": "Online Pharmacy Ordering API is running"
    }

@app.get("/health")
def health_check():
    return {
        "status": "OK"
    }