from datetime import datetime

from sqlalchemy import select
from typing import List, Optional
from db.controllers.TemplateController import Controller
from db.models.RequestModel import RequestModel
from sqlalchemy.ext.asyncio import AsyncSession

class RequestsController(Controller):
    async def get_all(self) -> List[RequestModel]:
        async with self.async_session() as session:
            query = select(RequestModel)
            result = await session.scalars(query)
            res: List[RequestModel] = result.all()
        return res

    async def get_by(
        self,
        id: Optional[int] = None,
        user_id: Optional[int] = None,
        tarif_id: Optional[int] = None,
        payment_id: Optional[int] = None,
        path_photo: Optional[str] = None,
        path_doc: Optional[str] = None,
        limit = None,
        offset = None,
        updated_at_start = None,
        updated_at_end = None,
        created_at_start = None,
        created_at_end = None
    ) -> List[RequestModel]:
        async with self.async_session() as session:
            query = select(RequestModel)
            if id is not None:
                query = query.where(RequestModel.id == id)
            if user_id is not None:
                query = query.where(RequestModel.user_id == user_id)
            if tarif_id is not None:
                query = query.where(RequestModel.tarif_id == tarif_id)
            if payment_id is not None:
                query = query.where(RequestModel.payment_id == payment_id)
            if path_photo is not None:
                query = query.where(RequestModel.path_photo == path_photo)
            if path_doc is not None:
                query = query.where(RequestModel.path_doc == path_doc)
            if updated_at_start is not None:
                query = query.where(RequestModel.updated_at >= updated_at_start)
            if updated_at_end is not None:
                query = query.where(RequestModel.updated_at <= updated_at_end)
            if created_at_start is not None:
                query = query.where(RequestModel.created_at >= created_at_start)
            if created_at_end is not None:
                query = query.where(RequestModel.created_at <= created_at_end)

            if limit is not None:
                query = query.limit(limit)
            if offset is not None:
                query = query.offset(offset)

            result = await session.scalars(query)
            res: List[RequestModel] = result.all()
        return res

    async def create(
        self, user_id: int, tarif_id: int, payment_id: int, path_photo: str, path_doc: str, updated_at = datetime.now(), created_at = datetime.now()
    ) -> RequestModel:
        async with self.async_session() as session:
            async with session.begin():
                tmp = RequestModel(
                    user_id=user_id, tarif_id=tarif_id, path_photo=path_photo, path_doc=path_doc, payment_id=payment_id,
                    updated_at=updated_at, created_at=created_at
                )
                session.add(tmp)
                await session.commit()
                #await session.refresh(tmp)
        return tmp

    async def delete(self, id: int) -> Optional[RequestModel]:
        async with self.async_session() as session:
            async with session.begin():
                query = select(RequestModel).where(RequestModel.id == id)
                result = await session.scalars(query)
                tmp: Optional[RequestModel] = result.first()
                if tmp:
                    await session.delete(tmp)
                    await session.commit()
        return tmp
