from db.models.BaseModel import BaseModel
from db.models.imports import *
from datetime import datetime

class PaymentModel(BaseModel):
    __tablename__ = 'payments'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))

    updated_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True))

    def __init__(self, name: str, description: str, updated_at: datetime, created_at: datetime):
        self.name = name
        self.description = description
        self.updated_at = updated_at
        self.created_at = created_at
