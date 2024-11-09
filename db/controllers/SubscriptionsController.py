from datetime import datetime

from sqlalchemy import select
from typing import List, Optional
from db.controllers.TemplateController import Controller
from db.models.SubscriptionModel import SubscriptionModel
from sqlalchemy.ext.asyncio import AsyncSession

class SubscriptionsController(Controller):
    async def get_all(self) -> List[SubscriptionModel]:
        async with self.async_session() as session:
            query = select(SubscriptionModel)
            result = await session.scalars(query)
            res: List[SubscriptionModel] = result.all()
        return res

    async def get_by(
        self,
        id: Optional[int] = None,
        user_id: Optional[int] = None,
        tarif_id: Optional[int] = None,
        limit = None,
        offset = None,
        date_to_start = None,
        date_to_end = None,
        updated_at_start = None,
        updated_at_end = None,
        created_at_start = None,
        created_at_end = None
    ) -> List[SubscriptionModel]:
        async with self.async_session() as session:
            query = select(SubscriptionModel)
            if id is not None:
                query = query.where(SubscriptionModel.id == id)
            if user_id is not None:
                query = query.where(SubscriptionModel.user_id == user_id)
            if tarif_id is not None:
                query = query.where(SubscriptionModel.tarif_id == tarif_id)
            if date_to_start is not None:
                query = query.where(SubscriptionModel.date_to >= date_to_start)
            if date_to_end is not None:
                query = query.where(SubscriptionModel.date_to <= date_to_end)
            if updated_at_start is not None:
                query = query.where(SubscriptionModel.updated_at >= updated_at_start)
            if updated_at_end is not None:
                query = query.where(SubscriptionModel.updated_at <= updated_at_end)
            if created_at_start is not None:
                query = query.where(SubscriptionModel.created_at >= created_at_start)
            if created_at_end is not None:
                query = query.where(SubscriptionModel.created_at <= created_at_end)

            if offset is not None:
                query = query.offset(offset)
            if limit is not None:
                query = query.limit(limit)

            result = await session.scalars(query)
            res: List[SubscriptionModel] = result.all()
        return res

    async def create(
        self, user_id: int, tarif_id: int, date_to, updated_at = datetime.now(), created_at = datetime.now()
    ) -> SubscriptionModel:
        async with self.async_session() as session:
            async with session.begin():
                tmp = SubscriptionModel(
                    user_id=user_id, tarif_id=tarif_id, date_to=date_to,
                    updated_at=updated_at, created_at=created_at
                )
                session.add(tmp)
                await session.commit()
                #await session.refresh(tmp)
        return tmp

    async def delete(self, id: int) -> Optional[SubscriptionModel]:
        async with self.async_session() as session:
            async with session.begin():
                query = select(SubscriptionModel).where(SubscriptionModel.id == id)
                result = await session.scalars(query)
                tmp: Optional[SubscriptionModel] = result.first()
                if tmp:
                    await session.delete(tmp)
                    await session.commit()
        return tmp
