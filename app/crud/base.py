from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class CRUDBase:
    def __init__(self, model):
        self.model = model

    async def get(self, object_id: int, session: AsyncSession):
        return (await session.execute(select(self.model).where(
            self.model.id == object_id)
        )).scalars().first()

    async def get_all(self, session: AsyncSession):
        return (await session.execute(select(self.model))).scalars().all()

    async def get_not_fully_invested(self, session: AsyncSession):
        return (await session.execute(select(self.model).where(
            self.model.fully_invested.is_(False)
        ).order_by(
            self.model.create_date
        ))).scalars().all()

    async def create(
        self,
        object,
        session: AsyncSession,
        commit: bool = True,
        user: Optional[User] = None,
    ):
        object_data = object.dict()
        if user is not None:
            object_data['user_id'] = user.id
        db_object = self.model(**object_data)
        session.add(db_object)
        if commit:
            await session.commit()
            await session.refresh(db_object)
        return db_object

    async def update(
            self,
            db_object,
            object_in,
            session: AsyncSession,
            commit: bool = True
    ):
        obj_data = jsonable_encoder(db_object)
        update_data = object_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_object, field, update_data[field])
        session.add(db_object)
        if commit:
            await session.commit()
            await session.refresh(db_object)
        return db_object

    async def remove(self, object, session: AsyncSession):
        await session.delete(object)
        await session.commit()
        return object
