import pytest
import os
os.environ["TESTING"] = "true"

from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, engine
import app.models as models

# Ініціалізація клієнта для тестування API
client = TestClient(app)


# Фікстура для очищення бази даних перед кожним тестом
@pytest.fixture(autouse=True)
def setup_database():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)


# Фікстура для створення тестової сесії бази даних
@pytest.fixture
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Тест для створення клієнта
def test_create_client():
    response = client.post(
        "/clients/",
        json={
            "name": "Тестовий Клієнт",
            "email": "test@example.com",
            "phone": "+380991234567",
            "is_active": True
        }
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"


# Тест для отримання списку клієнтів
def test_read_clients():
    # Створюємо клієнта
    client.post(
        "/clients/",
        json={
            "name": "Тестовий Клієнт",
            "email": "test@example.com",
            "phone": "+380991234567",
            "is_active": True
        }
    )
    response = client.get("/clients/")
    assert response.status_code == 200
    assert len(response.json()) > 0


# Тест для отримання клієнта за ID
def test_read_client():
    response = client.post(
        "/clients/",
        json={
            "name": "Тестовий Клієнт 2",
            "email": "test2@example.com",
            "phone": "+380991234568",
            "is_active": True
        }
    )
    client_id = response.json()["id"]
    response = client.get(f"/clients/{client_id}")
    assert response.status_code == 200
    assert response.json()["email"] == "test2@example.com"


# Тест для оновлення клієнта
def test_update_client():
    response = client.post(
        "/clients/",
        json={
            "name": "Тестовий Клієнт 3",
            "email": "test3@example.com",
            "phone": "+380991234569",
            "is_active": True
        }
    )
    client_id = response.json()["id"]
    response = client.put(
        f"/clients/{client_id}",
        json={"name": "Оновлений Клієнт"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Оновлений Клієнт"


# Тест для видалення клієнта
def test_delete_client():
    response = client.post(
        "/clients/",
        json={
            "name": "Тестовий Клієнт 4",
            "email": "test4@example.com",
            "phone": "+380991234570",
            "is_active": True
        }
    )
    client_id = response.json()["id"]
    response = client.delete(f"/clients/{client_id}")
    assert response.status_code == 200
    response = client.get(f"/clients/{client_id}")
    assert response.status_code == 404


# Тест для бізнес-логіки: клієнт не може мати два активних абонементи
def test_no_duplicate_active_subscriptions():
    # Створюємо клієнта
    response = client.post(
        "/clients/",
        json={
            "name": "Тестовий Клієнт 5",
            "email": "test5@example.com",
            "phone": "+380991234571",
            "is_active": True
        }
    )
    client_id = response.json()["id"]

    # Створюємо перший активний абонемент
    client.post(
        "/subscriptions/",
        json={
            "client_id": client_id,
            "subscription_type": "monthly",
            "start_date": "2025-04-01T00:00:00",
            "end_date": "2025-05-01T00:00:00",
            "price": 500.0,
            "is_active": True
        }
    )

    # Спроба створити другий активний абонемент
    response = client.post(
        "/subscriptions/",
        json={
            "client_id": client_id,
            "subscription_type": "yearly",
            "start_date": "2025-04-01T00:00:00",
            "end_date": "2026-04-01T00:00:00",
            "price": 5000.0,
            "is_active": True
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Client already has an active subscription"


# Тест для створення тренера
def test_create_trainer():
    response = client.post(
        "/trainers/",
        json={
            "name": "Тестовий Тренер",
            "email": "trainer@example.com",
            "phone": "+380991234572",
            "specialization": "Йога"
        }
    )
    assert response.status_code == 200
    assert response.json()["email"] == "trainer@example.com"