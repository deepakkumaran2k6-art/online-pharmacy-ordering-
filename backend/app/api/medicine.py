from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.medicine import Medicine


router = APIRouter(
    prefix="/medicines",
    tags=["Medicines"]
)


@router.post("/")
def create_medicine(
    category_id: int,
    medicine_name: str,
    description: str,
    price: float,
    stock_quantity: int,
    prescription_required: bool,
    db: Session = Depends(get_db)
):
    medicine = Medicine(
        category_id=category_id,
        medicine_name=medicine_name,
        description=description,
        price=price,
        stock_quantity=stock_quantity,
        prescription_required=prescription_required
    )

    db.add(medicine)
    db.commit()
    db.refresh(medicine)

    return {
        "message": "Medicine created successfully",
        "medicine_id": medicine.medicine_id,
        "category_id": medicine.category_id,
        "medicine_name": medicine.medicine_name,
        "description": medicine.description,
        "price": medicine.price,
        "stock_quantity": medicine.stock_quantity,
        "prescription_required": medicine.prescription_required
    }


@router.get("/")
def get_medicines(
    db: Session = Depends(get_db)
):
    medicines = db.query(Medicine).all()

    return medicines