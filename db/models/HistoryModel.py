from db.models.BaseModel import BaseModel
from db.models.imports import *
from datetime import datetime

class HistoryModel(BaseModel):
    __tablename__ = 'historys'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[str] = mapped_column(String(255))
    group_id: Mapped[str] = mapped_column(String(255))
    payment_id: Mapped[int] = mapped_column(Integer())
    date_to = Column(DateTime(timezone=True))

    updated_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True))

    def __init__(self, tg_id: str, group_id: str, payment_id: int, date_to: datetime, updated_at: datetime, created_at: datetime):
        self.tg_id = tg_id
        self.group_id = group_id
        self.payment_id = payment_id
        self.date_to = date_to
        self.updated_at = updated_at
        self.created_at = created_at
