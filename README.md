# Cat Charity - API сервис управления благотворительными проектами, пожертвованиями и пользователями на базе фреймворка FastAPI.

[![Python](https://img.shields.io/badge/-Python-3771a1?style=flat&logo=Python&logoColor=ffffff)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/-FastAPI-009688?style=flat&logo=FastAPI&logoColor=ffffff)](https://fastapi.tiangolo.com/)
[![FastAPI Users](https://img.shields.io/badge/-FastAPI--Users-B22222?style=flat&logo=fastapi&logoColor=ffffff)](https://fastapi-users.github.io/fastapi-users/)
[![SQLAlchemy](https://img.shields.io/badge/-SQLAlchemy-blue?style=flat&logo=sqlalchemy&logoColor=ffffff)](https://www.sqlalchemy.org/)
[![Google API](https://img.shields.io/badge/-Google%20API-4285F4?style=flat&logo=google&logoColor=ffffff)](https://developers.google.com/apis)


Автор – [Халин Вадим](https://t.me/gohub1)

---

## Оглавление
- [Описание](#описание)  
- [Основные технологии](#основные-технологии)
- [Интеграция с Google Scheets](#интеграция-с-Google-Scheets)
  - [Настройка](#настройка)
- [Запуск проекта](#запуск-проекта)

---

## Описание
Cat Charity — API сервис для управления благотворительными фондами.
Система позволяет:
- Создавать и редактировать проекты с указанной целью по сбору средств.
- Вносить пожертвования в проекты.
- Автоматически распределять пожертвования по незавершённым проектам (инвестирование).
- Отслеживать статус проектов и пожертвований (полностью собранные/закрытые).
- Управлять пользователями системы (регистрация, аутентификация, роли).
- Ограничивать доступ к операциям в зависимости от прав пользователя.

Проект написан на FastAPI с асинхронной работой базы данных через SQLAlchemy.

---

## Основные технологии
- Python
- FastAPI
- FastAPIUsers
- SQLAlchemy
- SQLite
- Pydantic
- Alembic

---

## Интеграция с Google Sheets
Сервис умеет автоматически формировать отчеты по фондам в Google Sheets.
При отправке суперпользователем POST /google/:
Таблица с данными: название, время сбора денег и описание появится у вас на аккаунте.
Название таблицы содердит сегодняшнюю дату, например: Отчет от 2026/01/16.

### Настройка
1. Создайте сервисный аккаунт в Google Cloud. (Role: Editor)
2. Подключите к вашему проекту Goodle Drive API и Google Sheets API.
3. Скачайте JSON ключ и укажите данные в .env.
```
EMAIL=admin@gmail.com

TYPE=service_account
PROJECT_ID=your_prject_id
PRIVATE_KEY_ID=your_private_key_id
PRIVATE_KEY="your_private_key"
CLIENT_EMAIL=your_client_email
CLIENT_ID=your_client_id
AUTH_URI=https://accounts.google.com/o/oauth2/auth
TOKEN_URI=https://oauth2.googleapis.com/token
AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/your_url

```
4. У вас должен получиться такой результат.

**Отчет от:** 2026/01/16 13:20:58  
**Топ проектов по скорости закрытия**

| Название проекта | Время сбора            | Описание                            |
|------------------|------------------------|-------------------------------------|
| Мурзик-Марафон   | 1 day 0:01:09.153931   | Сбор на шерстяные игрушки           |
| Кото-Экспресс    | 10 days 0:00:32.421910 | Срочная помощь пушистым спасателям  |
| Лапка счастья    | 11 days 0:00:28.499666 | Поддержка котиков из приюта         |

---

## Запуск проекта
1. Клонируем репозиторий.
```
git clone git@github.com:GohubSilently/cat_charity_spreadsheets.git && cd cat_charity_spreadsheets
```

2. Установливаем зависимости.
```
python3 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip && pip install -r requirements.tx
```

3. Настраиваем (.env).
```
APP_TITLE=Благотворительный фонд поддержки котиков QRKot
APP_DESCRIPTION=Сервис для поддержки котиков

DATABASE_URL=sqlite+aiosqlite:///./charity_fund.db

SECRET=secret_password
```

4. Запускаем миграции
```
alembic upgrade head
```

5. Инициализируем проект.
```
uvicorn app.main:app --reload
```

6.  Документация доступна:
- [Swagger UI](http://127.0.0.1:8000/docs)
- [ReDoc](http://127.0.0.1:8000/redoc)

---
