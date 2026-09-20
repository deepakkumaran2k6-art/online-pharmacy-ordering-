from sqlalchemy import Column, Integer, String, DateTime, func

from app.core.database import Base


class Prescription(Base):
    __tablename__ = "prescriptions"

    prescription_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        nullable=False
    )

    order_id = Column(
        Integer,
        nullable=False
    )

    file_path = Column(
        String(255),
        nullable=False
    )

    verification_status = Column(
        String(30),
        nullable=False,
        default="Pending"
    )

    uploaded_at = Column(
        DateTime,
        nullable=True,
        server_default=func.current_timestamp()
    )