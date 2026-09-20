import os
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.auth import get_current_user_payload
from app.models.prescription import Prescription
from app.models.order import Order


router = APIRouter(
    prefix="/prescriptions",
    tags=["Prescriptions"]
)


UPLOAD_DIR = "uploads/prescriptions"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_prescription(
    order_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user_payload)
):
    order = (
        db.query(Order)
        .filter(
            Order.order_id == order_id,
            Order.user_id == user.get("user_id")
        )
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    allowed_types = [
        "application/pdf",
        "image/jpeg",
        "image/png"
    ]

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, JPG and PNG files are allowed"
        )

    extension = os.path.splitext(file.filename)[1].lower()

    filename = f"{uuid.uuid4()}{extension}"

    file_path = os.path.join(
        UPLOAD_DIR,
        filename
    )

    file_content = await file.read()

    with open(file_path, "wb") as buffer:
        buffer.write(file_content)

    prescription = Prescription(
        user_id=user.get("user_id"),
        order_id=order_id,
        file_path=file_path,
        verification_status="Pending"
    )

    db.add(prescription)
    db.commit()
    db.refresh(prescription)

    return {
        "message": "Prescription uploaded successfully",
        "prescription_id": prescription.prescription_id,
        "order_id": prescription.order_id,
        "file_path": prescription.file_path,
        "verification_status": prescription.verification_status
    }