from db.models.BaseModel import BaseModel
from db.models.imports import *
from datetime import datetime

class TarifModel(BaseModel):
    __tablename__ = 'tarifs'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))
    group_id: Mapped[str] = mapped_column(String(255))
    days: Mapped[int] = mapped_column(Integer())
    mouths: Mapped[int] = mapped_column(Integer())
    invite_link: Mapped[str] = mapped_column(String(255))

    updated_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True))

    def __init__(self, name: str, description: str, group_id: str, days: int, mouths: int, invite_link: str, updated_at: datetime, created_at: datetime):
        self.name = name
        self.description = description
        self.group_id = group_id
        self.days = days
        self.mouths = mouths
        self.invite_link = invite_link
        self.updated_at = updated_at
        self.created_at = created_at
