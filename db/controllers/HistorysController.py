from datetime import datetime

from sqlalchemy import select
from typing import List, Optional
from db.controllers.TemplateController import Controller
from db.models.HistoryModel import HistoryModel
from sqlalchemy.ext.asyncio import AsyncSession

class HistorysController(Controller):
    async def get_all(self) -> List[HistoryModel]:
        async with self.async_session() as session:
            query = select(HistoryModel)
            result = await session.scalars(query)
            res: List[HistoryModel] = result.all()
        return res

    async def get_by(
        self,
        id: Optional[int] = None,
        tg_id: Optional[str] = None,
        group_id: Optional[str] = None,
        payment_id: Optional[int] = None,
        date_to_start = None,
        date_to_end = None,
        updated_at_start = None,
        updated_at_end = None,
        created_at_start = None,
        created_at_end = None
    ) -> List[HistoryModel]:
        async with self.async_session() as session:
            query = select(HistoryModel)
            if id is not None:
                query = query.where(HistoryModel.id == id)
            if tg_id is not None:
                query = query.where(HistoryModel.tg_id == tg_id)
            if group_id is not None:
                query = query.where(HistoryModel.group_id == group_id)
            if payment_id is not None:
                query = query.where(HistoryModel.payment_id == payment_id)
            if date_to_start is not None:
                query = query.where(HistoryModel.date_to >= date_to_start)
            if date_to_end is not None:
                query = query.where(HistoryModel.date_to <= date_to_end)
            if updated_at_start is not None:
                query = query.where(HistoryModel.updated_at >= updated_at_start)
            if updated_at_end is not None:
                query = query.where(HistoryModel.updated_at <= updated_at_end)
            if created_at_start is not None:
                query = query.where(HistoryModel.created_at >= created_at_start)
            if created_at_end is not None:
                query = query.where(HistoryModel.created_at <= created_at_end)

            result = await session.scalars(query)
            res: List[HistoryModel] = result.all()
        return res

    async def create(
        self, tg_id: str, group_id: str, payment_id: int, date_to, updated_at = datetime.now(), created_at = datetime.now()
    ) -> HistoryModel:
        async with self.async_session() as session:
            async with session.begin():
                tmp = HistoryModel(
                    tg_id=tg_id, group_id=group_id, payment_id=payment_id, date_to=date_to,
                    updated_at=updated_at, created_at=created_at
                )
                session.add(tmp)
                await session.commit()
                #await session.refresh(tmp)
        return tmp

    async def delete(self, id: int) -> Optional[HistoryModel]:
        async with self.async_session() as session:
            async with session.begin():
                query = select(HistoryModel).where(HistoryModel.id == id)
                result = await session.scalars(query)
                tmp: Optional[HistoryModel] = result.first()
                if tmp:
                    await session.delete(tmp)
                    await session.commit()
        return tmp
