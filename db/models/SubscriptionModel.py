from db.models.BaseModel import BaseModel
from db.models.imports import *
from datetime import datetime

class SubscriptionModel(BaseModel):
    __tablename__ = 'subscriptions'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer())
    tarif_id: Mapped[int] = mapped_column(Integer())
    date_to =  Column(DateTime(timezone=True))

    updated_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True))

    def __init__(self, user_id: int, tarif_id: int, date_to, updated_at: datetime, created_at: datetime):
        self.user_id = user_id
        self.tarif_id = tarif_id
        self.date_to = date_to
        self.updated_at = updated_at
        self.created_at = created_at
