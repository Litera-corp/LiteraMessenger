# tests/test_integration_registration.py
import os
import subprocess
import time
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text

from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker

load_dotenv()


# Утилита: получаем URL тестовой БД из окружения
def _get_db_url():
    return os.getenv("TEST_DATABASE_URL")

@pytest.fixture(scope="session")
def db_url():
    url = _get_db_url()
    if not url:
        pytest.skip("TEST_DATABASE_URL / DATABASE_URL not set — skipping integration tests")
    return url

@pytest.fixture(scope="session", autouse=True)
def apply_migrations(db_url):
    """
    Применяем миграции перед тестовой сессией и откатываем в конце.
    Требует, чтобы alembic был в PATH и DATABASE_URL/TEST_DATABASE_URL корректно установлен.
    """
    env = os.environ.copy()
    env["TEST_DATABASE_URL"] = db_url
    env["DATABASE_URL"] = db_url

    # apply migrations
    subprocess.run(["alembic", "upgrade", "head"], check=True, env=env)

    # небольшая пауза, чтобы убедиться в готовности (иногда полезно)
    time.sleep(0.5)

    yield

    # откатываем к base (чистим)
    subprocess.run(["alembic", "downgrade", "base"], check=True, env=env)

@pytest.fixture
def client(db_url, apply_migrations, monkeypatch):
    monkeypatch.setenv("TEST_DATABASE_URL", db_url)
    monkeypatch.setenv("DATABASE_URL", db_url)
    from main import app

    return TestClient(app)

def test_registration_success_creates_user_and_returns_token(client, db_url):
    email = f"integration_{int(time.time())}@example.com"
    payload = {
        "email": email,
        "password": "IntPass123!",
        "username": "intuser",
        "display_name": "Integration User"
    }

    r = client.post("/users/register", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "user" in data
    assert data["user"]["email"] == email

    # Проверяем, что запись действительно в БД (schema users)
    print(db_url)
    engine = create_engine(db_url)
    with engine.connect() as conn:
        row = conn.execute(
            text("SELECT id, email, password_hash FROM users.users WHERE email = :email"),
            {"email": email}
        ).mappings().fetchone()

        assert row is not None
        assert row["email"] == email
        password_hash = row["password_hash"]
        # Пароль в БД не равен открытому
        assert password_hash != payload["password"]

        # Дополнительно проверим verify_password util
        from app.utils import verify_password
        assert verify_password(payload["password"], password_hash) is True

def test_registration_conflict_returns_409(client, db_url):
    # Создадим пользователя напрямую, затем попробуем зарегистрировать с тем же email
    email = f"conflict_{int(time.time())}@example.com"
    payload = {
        "email": email,
        "password": "ConfPass123!",
        "username": "conflictuser"
    }

    r1 = client.post("/users/register", json=payload)
    assert r1.status_code == 201, r1.text

    r2 = client.post("/users/register", json=payload)
    assert r2.status_code == 409
    assert r2.json().get("detail") is not None

def test_registration_validation_returns_422(client):
    r = client.post("/users/register", json={})
    assert r.status_code == 422

def test_registration_password_validation_returns_422(client, db_url):
    email = f"conflict_pass_{int(time.time())}@example.com"
    payload = {
        "email": email,
        "password": "strpass",
        "username": "conflictpassuser"
    }

    r = client.post("/users/register", json=payload)
    assert r.status_code == 422
    assert r.json().get("detail") is not None
