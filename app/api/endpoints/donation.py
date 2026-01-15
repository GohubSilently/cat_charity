from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.charity import charity_crud
from app.crud.donation import donation_crud
from app.models import User
from app.services.logic import allocate
from app.schemas.donation import DonationCreate, DonationDB, DonationFullInfoDB


router = APIRouter()


SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.get(
    '/',
    response_model=list[DonationFullInfoDB],
    description='Показать список всех пожертвований.',
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: SessionDep
):
    """
    Только для суперпользователей.
    """
    return await donation_crud.get_all(session)


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    description='Показать список пожертвований пользователя, '
                'выполняющего запрос.'
)
async def get_user_donations(
    session: SessionDep,
    user: Annotated[User, Depends(current_user)],
):
    """
    Только для зарегистрированных пользователей.
    """
    return await donation_crud.get_user_donation(session, user)


@router.post(
    '/',
    response_model=DonationDB,
    description='Создать пожертвование.',
    response_model_exclude_none=True,
    response_model_exclude={'user_id'}
)
async def create_donation(
    donation: DonationCreate,
    session: SessionDep,
    user: Annotated[User, Depends(current_user)],
):
    """
    Для зарегистрированных пользователей и суперпользователей.
    """
    donation = await donation_crud.create(
        donation, session, commit=False, user=user
    )
    session.add_all(allocate(
        donation, await charity_crud.get_not_fully_invested(session)
    ))
    await session.commit()
    await session.refresh(donation)
    return donation
