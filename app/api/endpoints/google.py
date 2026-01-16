from http import HTTPStatus

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends, HTTPException
from pydantic_core import ErrorDetails
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity import charity_crud
from app.services.google import (
    create_spreadsheets, set_user_permissions,
    update_spreadsheets_value
)


router = APIRouter()


@router.post(
    '/',
    response_model=str,
    dependencies=[Depends(current_superuser)]
)
async def get_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service)
):
    """Только для суперпользователей."""
    charity_projects = await charity_crud.get_projects_by_completion_rate(
        session
    )
    spreadsheet_id, link = await create_spreadsheets(wrapper_services)
    await set_user_permissions(spreadsheet_id, wrapper_services)
    try:
        await update_spreadsheets_value(
            spreadsheet_id,
            charity_projects,
            wrapper_services
        )
    except HTTPException as error:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail=error
        )
    return link
