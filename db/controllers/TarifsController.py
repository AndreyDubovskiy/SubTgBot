from datetime import datetime

from sqlalchemy import select
from typing import List, Optional
from db.controllers.TemplateController import Controller
from db.models.TarifModel import TarifModel
from sqlalchemy.ext.asyncio import AsyncSession

class TarifsController(Controller):
    async def get_all(self) -> List[TarifModel]:
        async with self.async_session() as session:
            query = select(TarifModel)
            result = await session.scalars(query)
            res: List[TarifModel] = result.all()
        return res

    async def get_by(
        self,
        id: Optional[int] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        group_id: Optional[str] = None,
        days: Optional[int] = None,
        mouths: Optional[int] = None,
        invite_link: Optional[str] = None,
        offset = None,
        limit = None,
        updated_at_start = None,
        updated_at_end = None,
        created_at_start = None,
        created_at_end = None
    ) -> List[TarifModel]:
        async with self.async_session() as session:
            query = select(TarifModel)
            if id is not None:
                query = query.where(TarifModel.id == id)
            if name is not None:
                query = query.where(TarifModel.name == name)
            if description is not None:
                query = query.where(TarifModel.description == description)
            if group_id is not None:
                query = query.where(TarifModel.group_id == group_id)
            if invite_link is not None:
                query = query.where(TarifModel.invite_link == invite_link)
            if days is not None:
                query = query.where(TarifModel.days == days)
            if mouths is not None:
                query = query.where(TarifModel.mouths == mouths)
            if updated_at_start is not None:
                query = query.where(TarifModel.updated_at >= updated_at_start)
            if updated_at_end is not None:
                query = query.where(TarifModel.updated_at <= updated_at_end)
            if created_at_start is not None:
                query = query.where(TarifModel.created_at >= created_at_start)
            if created_at_end is not None:
                query = query.where(TarifModel.created_at <= created_at_end)

            if offset is not None:
                query = query.offset(offset)
            if limit is not None:
                query = query.limit(limit)

            result = await session.scalars(query)
            res: List[TarifModel] = result.all()
        return res

    async def create(
        self, name: str, description: str, group_id: str, days: int, mouths: int, invite_link: str, updated_at = datetime.now(), created_at = datetime.now()
    ) -> TarifModel:
        async with self.async_session() as session:
            async with session.begin():
                tmp = TarifModel(
                    name=name, description=description, group_id=group_id, days=days, mouths=mouths, invite_link=invite_link,
                    updated_at=updated_at, created_at=created_at
                )
                session.add(tmp)
                await session.commit()
                #await session.refresh(tmp)
        return tmp

    async def delete(self, id: int) -> Optional[TarifModel]:
        async with self.async_session() as session:
            async with session.begin():
                query = select(TarifModel).where(TarifModel.id == id)
                result = await session.scalars(query)
                tmp: Optional[TarifModel] = result.first()
                if tmp:
                    await session.delete(tmp)
                    await session.commit()
        return tmp
