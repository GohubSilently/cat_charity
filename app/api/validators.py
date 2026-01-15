from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity import charity_crud


async def check_unique_name(
    name: str,
    session: AsyncSession
):
    if charity_project := await charity_crud.get_name(name, session):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!'
        )
    return charity_project


async def check_full_amount(
    charity_id: int,
    update_amount: int,
    session: AsyncSession
):
    charity_project = await charity_crud.get(charity_id, session)
    if update_amount < charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя установить значение full_amount меньше '
                   'уже вложенной суммы.'
        )
    return charity_project


async def check_charity_project_exists(
    charity_project_id: int,
    session: AsyncSession,
):
    charity_project = await charity_crud.get(charity_project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Благотворительного проекта не существует!',
        )
    return charity_project


def check_fully_invested_amount(
    fully_invested: bool
):
    if fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )


def check_invested_amount(
    invested_amount: int
):
    if invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
