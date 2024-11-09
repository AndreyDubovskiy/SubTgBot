from db.models.BaseModel import BaseModel
from db.models.imports import *
from datetime import datetime

class UserModel(BaseModel):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[str] = mapped_column(String(255))
    username: Mapped[str] = mapped_column(String(255), nullable=True)

    updated_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True))

    def __init__(self, tg_id: str, username: str, updated_at: datetime, created_at: datetime):
        self.tg_id = tg_id
        self.username = username
        self.updated_at = updated_at
        self.created_at = created_at
