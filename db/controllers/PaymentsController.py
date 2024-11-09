from datetime import datetime

from sqlalchemy import select
from typing import List, Optional
from db.controllers.TemplateController import Controller
from db.models.PaymentModel import PaymentModel
from sqlalchemy.ext.asyncio import AsyncSession

class PaymentsController(Controller):
    async def get_all(self) -> List[PaymentModel]:
        async with self.async_session() as session:
            query = select(PaymentModel)
            result = await session.scalars(query)
            res: List[PaymentModel] = result.all()
        return res

    async def get_by(
        self,
        id: Optional[int] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        updated_at_start = None,
        updated_at_end = None,
        created_at_start = None,
        created_at_end = None,
        offset = None,
        limit = None
    ) -> List[PaymentModel]:
        async with self.async_session() as session:
            query = select(PaymentModel)
            if id is not None:
                query = query.where(PaymentModel.id == id)
            if name is not None:
                query = query.where(PaymentModel.name == name)
            if description is not None:
                query = query.where(PaymentModel.description == description)
            if updated_at_start is not None:
                query = query.where(PaymentModel.updated_at >= updated_at_start)
            if updated_at_end is not None:
                query = query.where(PaymentModel.updated_at <= updated_at_end)
            if created_at_start is not None:
                query = query.where(PaymentModel.created_at >= created_at_start)
            if created_at_end is not None:
                query = query.where(PaymentModel.created_at <= created_at_end)

            if offset is not None:
                query = query.offset(offset)
            if limit is not None:
                query = query.limit(limit)

            result = await session.scalars(query)
            res: List[PaymentModel] = result.all()
        return res

    async def create(
        self, name: str, description: str, updated_at = datetime.now(), created_at = datetime.now()
    ) -> PaymentModel:
        async with self.async_session() as session:
            async with session.begin():
                tmp = PaymentModel(
                    name=name, description=description,
                    updated_at=updated_at, created_at=created_at
                )
                session.add(tmp)
                await session.commit()
                #await session.refresh(tmp)
        return tmp

    async def delete(self, id: int) -> Optional[PaymentModel]:
        async with self.async_session() as session:
            async with session.begin():
                query = select(PaymentModel).where(PaymentModel.id == id)
                result = await session.scalars(query)
                tmp: Optional[PaymentModel] = result.first()
                if tmp:
                    await session.delete(tmp)
                    await session.commit()
        return tmp
