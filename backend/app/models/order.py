from sqlalchemy import Column, Integer, String, Numeric, DateTime, func

from app.core.database import Base


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False, default=0.00)
    order_status = Column(String(30), nullable=False, default="Placed")
    delivery_address = Column(String(255), nullable=False)
    order_date = Column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp()
    )