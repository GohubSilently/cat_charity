from sqlalchemy import select, desc, extract
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharity(CRUDBase):
    async def get_name(
        self,
        name: str,
        session: AsyncSession
    ):
        return (await session.execute(select(self.model).where(
            self.model.name == name)
        )).scalars().first()

    async def get_charity(
        self,
        session: AsyncSession
    ):
        statement = select(self.model).order_by(
            desc(self.model.fully_invested),
            desc(self.model.created_date)
        )
        return (await session.execute(statement)).scalars().first()

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession
    ):
        start = (
            extract('year', self.model.create_date) * 365 +
            extract('month', self.model.create_date) * 30 +
            extract('day', self.model.create_date)
        )
        end = (
            extract('year', self.model.close_date) * 365 +
            extract('month', self.model.close_date) * 30 +
            extract('day', self.model.close_date)
        )
        charity_projects = await session.execute(select(
            self.model.name,
            end - start,
            self.model.description
        ).where(
            self.model.fully_invested is True
        ).order_by(end - start))
        return [
            {
                'name': name,
                'time': time,
                'description': description
            } for name, time, description in charity_projects.all()
        ]


charity_crud = CRUDCharity(CharityProject)
