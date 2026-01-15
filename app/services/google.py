from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings

SHORT_FORMAT = '%Y/%m/%d'
FULL_FORMAT = f'{SHORT_FORMAT} %H:%M:%S'


async def create_spreadsheets(wrapper_services: Aiogoogle) -> str:
    current_date = datetime.now().strftime(SHORT_FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = {
        'properties': {
            'title': f'Отчет на {current_date}',
            'locale': 'ru_RU'
        },
        'sheets': [{
            'properties': {
                'sheetType': 'GRID',
                'sheetId': 0,
                'title': 'QRKot',
                'gridProperties': {
                    'rowCount': 100,
                    'columnCount': 5
                }
            }
        }]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(
    spreadsheetid: str,
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
             fileId=spreadsheetid,
             json=permissions_body,
             fields='id'
         )
     )


async def update_spreadsheets_value(
    spreadsheetid: str,
    charity_project: list,
    wrapper_services: Aiogoogle
):
    current_date = datetime.now().strftime(FULL_FORMAT)
    service = await wrapper_services.discover(
        'sheets', 'v4'
    )
    table_values = [
        ['Отчет от', f'{current_date}'],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
    for charity in charity_project:
        table_values.append(
            [
                str(charity['name']),
                str(charity['time']),
                str(charity['description'])
            ]
        )
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.value.update(
            spreadsheetId=spreadsheetid,
            range=f'A1:E{len(table_values)}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )