from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_exists, check_unique_name, check_full_amount,
    check_fully_invested_amount, check_invested_amount
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity import charity_crud
from app.crud.donation import donation_crud
from app.models import User
from app.services.logic import allocate
from app.schemas.charity import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)


router = APIRouter()
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    description='Показать список всех целевых проектов.',
    response_model_exclude_none=True
)
async def get_all_charity_projects(
    session: SessionDep
):
    """
    Для всех пользователей.
    """
    return await charity_crud.get_all(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    description='Создать целевой проект.',
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: SessionDep,
    user: Annotated[User, Depends(current_superuser)]
):
    """
    Только для суперпользователей.
    """
    await check_unique_name(charity_project.name, session)
    charity_project = await charity_crud.create(
        charity_project, session, commit=False
    )
    session.add_all(allocate(
        charity_project, await donation_crud.get_not_fully_invested(session)
    ))
    await session.commit()
    await session.refresh(charity_project)
    return charity_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    description='Редактировать целевой проект. '
                'Закрытый проект нельзя редактировать; нельзя установить '
                'требуемую сумму меньше уже вложенной.',
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int,
    charity_project: CharityProjectUpdate,
    session: SessionDep,
):
    """
    Только для суперпользователей.
    """
    charity = await check_charity_project_exists(project_id, session)
    await check_unique_name(charity_project.name, session)
    check_fully_invested_amount(charity.fully_invested)
    charity = await check_full_amount(
        charity.id, charity_project.full_amount, session
    )
    if charity.invested_amount == charity_project.full_amount:
        charity.fully_invested = True
        charity.close_date = datetime.now()
    return await charity_crud.update(charity, charity_project, session)


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    description='Удалить целевой проект. '
                'Нельзя удалить проект, в который уже '
                'были инвестированы средства.',
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project_id: int,
    session: SessionDep
):
    """
    Только для суперпользователей.
    """
    charity_project = await check_charity_project_exists(project_id, session)
    check_invested_amount(charity_project.invested_amount)
    return await charity_crud.remove(charity_project, session)
