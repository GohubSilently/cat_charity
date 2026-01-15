from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import User
from app.models.donation import Donation


class CRUDDonation(CRUDBase):
    async def get_user_donation(
        self,
        session: AsyncSession,
        user: User,
    ):
        return (await session.execute(select(Donation).where(
            Donation.user_id == user.id
        ))).scalars().all()


donation_crud = CRUDDonation(Donation)
