from sqlalchemy import Column, Integer, String, Text, Float, Boolean

from app.core.database import Base


class Medicine(Base):
    __tablename__ = "medicines"

    medicine_id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, nullable=False)
    medicine_name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, nullable=False, default=0)
    prescription_required = Column(Boolean, default=False)