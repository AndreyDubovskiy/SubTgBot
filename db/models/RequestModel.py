from db.models.BaseModel import BaseModel
from db.models.imports import *
from datetime import datetime

class RequestModel(BaseModel):
    __tablename__ = 'requests'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer())
    tarif_id: Mapped[int] = mapped_column(Integer())
    payment_id: Mapped[int] = mapped_column(Integer())
    path_photo: Mapped[str] = mapped_column(String(255), nullable=True)
    path_doc: Mapped[str] = mapped_column(String(255), nullable=True)

    updated_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True))

    def __init__(self, user_id: int, tarif_id: int, payment_id: int, updated_at: datetime, created_at: datetime, path_photo: str = None, path_doc: str = None):
        self.user_id = user_id
        self.tarif_id = tarif_id
        self.payment_id = payment_id
        self.path_photo = path_photo
        self.path_doc = path_doc
        self.updated_at = updated_at
        self.created_at = created_at
