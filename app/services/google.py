from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings


SHORT_FORMAT = '%Y/%m/%d'
FULL_FORMAT = f'{SHORT_FORMAT} %H:%M:%S'
ROW = 100
COLUMN = 5

BODY = dict(
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
                rowCount=ROW,
                columnCount=COLUMN
            )
        )
    )]
)

HEADER = [
    [('Отчет от', '{current_date}')],
    [('Топ проектов по скорости закрытия',)],
    [('Название проекта', 'Время сбора', 'Описание')]
]


async def create_spreadsheets(wrapper_services: Aiogoogle) -> str:
    current_date = datetime.now().strftime(SHORT_FORMAT)
    service = await wrapper_services.discover(
        'sheets', 'v4'
    )
    BODY['properties']['title'] = BODY['properties']['title'].format(
        current_date=current_date
    )
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=BODY)
    )
    return response['spreadsheetId'], response['url']


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
    HEADER[0][1] = HEADER[0][1].format(current_date=current_date)
    table_values = [
        *HEADER,
        *[list(
            map(
                str, (name, close_date - create_date, description)
            )
        ) for name, create_date, close_date, description in charity_project]
    ]
    if len(table_values) > ROW or len(charity_project) > COLUMN:
        raise ValueError(
            'Объем входных данных: '
            f'cтрок - {len(table_values)}, колонок - {len(table_values)} '
            f'превышает заданные знеачения: строк - {ROW}, колонок - {COLUMN}.'
        )
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{str(len(table_values))}'
                  f'C{str(len(charity_project))}',
            valueInputOption='USER_ENTERED',
            json={
                'majorDimension': 'ROWS',
                'values': table_values
            }
        )
    )
