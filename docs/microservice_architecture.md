## Базовая архитектура каждого микросервиса

```
service_name/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Точка входа приложения (FastAPI instance)
│   ├── config.py               # Настройки приложения (Pydantic BaseSettings)
│   ├── database.py             # Подключение PostgreSQL (SQLAlchemy + Alembic)
│   ├── kafka.py                # Настройка Kafka producer/consumer (aiokafka)
│   ├── redis.py                # Подключение Redis (aioredis)
│   ├── models.py               # Все SQLAlchemy модели
│   ├── schemas.py              # Все Pydantic DTO (input/output)
│   ├── routes.py               # FastAPI роуты
│   ├── services.py             # Основная бизнес-логика
│   ├── repository.py           # CRUD-операции для PostgreSQL
│   ├── consumers.py            # Kafka consumer таски (обработка событий)
│   ├── utils.py                # Вспомогательные функции
│   ├── exceptions.py           # Кастомные исключения и обработчики ошибок
│   └── ws.py                   # WebSocket-эндпоинты и менеджер соединений
│
├── alembic/                    # Миграции базы данных
│   ├── env.py
│   └── versions/
│
├── tests/                      # Unit и интеграционные тесты
│   ├── __init__.py
│   ├── test_routes.py
│   └── test_services.py
│
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── main.py                     # Точка входа приложения (FastAPI instance)
├── .env.example
├── requirements.txt
└── README.md
```

> ! Данная архитектура является базовой и может быть изменена в процессе работы