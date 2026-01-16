from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings


SHORT_FORMAT = '%Y/%m/%d'
FULL_FORMAT = f'{SHORT_FORMAT} %H:%M:%S'

BODY_CONST = dict(
    properties=dict(
        title='Отчет от {current_date}',
        locale='ru_RU',
    ),
    sheets=[dict(
        properties=dict(
            sheetType='GRID',
            sheetId=0,
            title='QRKot',
            gridProperties=dict(
                rowCount=100,
                columnCount=5
            )
        )
    )]
)

VALUES_CONST = list(
    (
        list(['Отчет от', '{current_date}']),
        list(['Топ проектов по скорости закрытия']),
        list(['Название проекта', 'Время сбора', 'Описание'])
    )
)

ROW = BODY_CONST['sheets'][0]['properties']['gridProperties']['rowCount']
COLUMN = BODY_CONST['sheets'][0]['properties']['gridProperties']['columnCount']
RANGE = f'R1C1:R{str(ROW)}C{str(COLUMN)}'


async def create_spreadsheets(wrapper_services: Aiogoogle) -> str:
    current_date = datetime.now().strftime(SHORT_FORMAT)
    service = await wrapper_services.discover(
        'sheets', 'v4'
    )
    body_copy = BODY_CONST.copy()
    body_copy['properties']['title'] = body_copy['properties']['title'].format(
        current_date=current_date
    )
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=BODY_CONST)
    )
    full_url = (f'https://docs.google.com/spreadsheets/d/'
                f'{response["spreadsheetId"]}')
    return response['spreadsheetId'], full_url


async def set_user_permissions(
    spreadsheet_id: str,
    wrapper_services: Aiogoogle
) -> None:
     permissions_body = {  # noqa E111
         'type': 'user',
         'role': 'writer',
         'emailAddress': settings.email
     }
     service = await wrapper_services.discover(  # noqa E111
         'drive', 'v3'
     )
     await wrapper_services.as_service_account(  # noqa E111
         service.permissions.create(
             fileId=spreadsheet_id,
             json=permissions_body,
             fields='id'
         )
     )


async def update_spreadsheets_value(
    spreadsheet_id: str,
    charity_project: list,
    wrapper_services: Aiogoogle
):
    current_date = datetime.now().strftime(FULL_FORMAT)
    service = await wrapper_services.discover(
        'sheets', 'v4'
    )
    VALUES_CONST[0][1] = current_date
    table_values = [
        *VALUES_CONST,
        *[list(
            map(
                str, (charity[0], charity[2] - charity[1], charity[3])
            )
        ) for charity in charity_project]
    ]
    if len(table_values) > ROW:
        raise ValueError('Объем данных превышает количество строк!')
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=RANGE,
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
