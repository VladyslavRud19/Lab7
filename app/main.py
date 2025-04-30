import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import logging
from typing import List, Optional
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import engine, get_db

# Налаштування логування
logging.basicConfig(
    filename="api.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fitness Center API",
    description="API для управління фітнес-центром",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# API ендпоінти для клієнтів
@app.post("/clients/", response_model=schemas.Client, tags=["Clients"])
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    logger.debug(f"Вхідні дані для створення клієнта: {client.dict()}")
    db_client = crud.get_client_by_email(db, email=client.email)
    if db_client:
        logger.warning(f"Спроба створити клієнта з уже зареєстрованим email: {client.email}")
        raise HTTPException(status_code=400, detail="Email already registered")
    result = crud.create_client(db=db, client=client)
    logger.info(f"Клієнт створений: {result.id}")
    return result


@app.get("/clients/", response_model=List[schemas.Client], tags=["Clients"])
def read_clients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info(f"Запит на отримання клієнтів: skip={skip}, limit={limit}")
    clients = crud.get_clients(db, skip=skip, limit=limit)
    logger.info(f"Повернуто {len(clients)} клієнтів")
    return clients


@app.get("/clients/{client_id}", response_model=schemas.Client, tags=["Clients"])
def read_client(client_id: int, db: Session = Depends(get_db)):
    logger.info(f"Запит на отримання клієнта: id={client_id}")
    db_client = crud.get_client(db, client_id=client_id)
    if db_client is None:
        logger.warning(f"Клієнт не знайдений: id={client_id}")
        raise HTTPException(status_code=404, detail="Client not found")
    return db_client


@app.put("/clients/{client_id}", response_model=schemas.Client, tags=["Clients"])
def update_client(client_id: int, client: schemas.ClientUpdate, db: Session = Depends(get_db)):
    logger.debug(f"Оновлення клієнта: id={client_id}, дані={client.dict()}")
    db_client = crud.update_client(db, client_id=client_id, client=client)
    if db_client is None:
        logger.warning(f"Клієнт не знайдений для оновлення: id={client_id}")
        raise HTTPException(status_code=404, detail="Client not found")
    logger.info(f"Клієнт оновлений: id={client_id}")
    return db_client


@app.delete("/clients/{client_id}", response_model=schemas.Client, tags=["Clients"])
def delete_client(client_id: int, db: Session = Depends(get_db)):
    logger.info(f"Видалення клієнта: id={client_id}")
    db_client = crud.delete_client(db, client_id=client_id)
    if db_client is None:
        logger.warning(f"Клієнт не знайдений для видалення: id={client_id}")
        raise HTTPException(status_code=404, detail="Client not found")
    logger.info(f"Клієнт видалений: id={client_id}")
    return db_client


@app.post("/trainers/", response_model=schemas.Trainer, tags=["Trainers"])
def create_trainer(trainer: schemas.TrainerCreate, db: Session = Depends(get_db)):
    logger.debug(f"Вхідні дані для створення тренера: {trainer.dict()}")
    db_trainer = crud.get_trainer_by_email(db, email=trainer.email)
    if db_trainer:
        logger.warning(f"Спроба створити тренера з уже зареєстрованим email: {trainer.email}")
        raise HTTPException(status_code=400, detail="Email already registered")
    result = crud.create_trainer(db=db, trainer=trainer)
    logger.info(f"Тренер створений: {result.id}")
    return result


@app.get("/trainers/", response_model=List[schemas.Trainer], tags=["Trainers"])
def read_trainers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info(f"Запит на отримання тренерів: skip={skip}, limit={limit}")
    trainers = crud.get_trainers(db, skip=skip, limit=limit)
    logger.info(f"Повернуто {len(trainers)} тренерів")
    return trainers


@app.get("/trainers/{trainer_id}", response_model=schemas.Trainer, tags=["Trainers"])
def read_trainer(trainer_id: int, db: Session = Depends(get_db)):
    logger.info(f"Запит на отримання тренера: id={trainer_id}")
    db_trainer = crud.get_trainer(db, trainer_id=trainer_id)
    if db_trainer is None:
        logger.warning(f"Тренер не знайдений: id={trainer_id}")
        raise HTTPException(status_code=404, detail="Trainer not found")
    return db_trainer


@app.put("/trainers/{trainer_id}", response_model=schemas.Trainer, tags=["Trainers"])
def update_trainer(trainer_id: int, trainer: schemas.TrainerUpdate, db: Session = Depends(get_db)):
    logger.debug(f"Оновлення тренера: id={trainer_id}, дані={trainer.dict()}")
    db_trainer = crud.update_trainer(db, trainer_id=trainer_id, trainer=trainer)
    if db_trainer is None:
        logger.warning(f"Тренер не знайдений для оновлення: id={trainer_id}")
        raise HTTPException(status_code=404, detail="Trainer not found")
    logger.info(f"Тренер оновлений: id={trainer_id}")
    return db_trainer


@app.delete("/trainers/{trainer_id}", response_model=schemas.Trainer, tags=["Trainers"])
def delete_trainer(trainer_id: int, db: Session = Depends(get_db)):
    logger.info(f"Видалення тренера: id={trainer_id}")
    db_trainer = crud.delete_trainer(db, trainer_id=trainer_id)
    if db_trainer is None:
        logger.warning(f"Тренер не знайдений для видалення: id={trainer_id}")
        raise HTTPException(status_code=404, detail="Trainer not found")
    logger.info(f"Тренер видалений: id={trainer_id}")
    return db_trainer


@app.post("/subscriptions/", response_model=schemas.Subscription, tags=["Subscriptions"])
def create_subscription(subscription: schemas.SubscriptionCreate, db: Session = Depends(get_db)):
    logger.debug(f"Вхідні дані для створення абонементу: {subscription.dict()}")
    result = crud.create_subscription(db=db, subscription=subscription)
    logger.info(f"Абонемент створений: {result.id}")
    return result


@app.get("/subscriptions/", response_model=List[schemas.Subscription], tags=["Subscriptions"])
def read_subscriptions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info(f"Запит на отримання абонементів: skip={skip}, limit={limit}")
    subscriptions = crud.get_subscriptions(db, skip=skip, limit=limit)
    logger.info(f"Повернуто {len(subscriptions)} абонементів")
    return subscriptions


@app.get("/subscriptions/{subscription_id}", response_model=schemas.Subscription, tags=["Subscriptions"])
def read_subscription(subscription_id: int, db: Session = Depends(get_db)):
    logger.info(f"Запит на отримання абонементу: id={subscription_id}")
    db_subscription = crud.get_subscription(db, subscription_id=subscription_id)
    if db_subscription is None:
        logger.warning(f"Абонемент не знайдений: id={subscription_id}")
        raise HTTPException(status_code=404, detail="Subscription not found")
    return db_subscription


@app.put("/subscriptions/{subscription_id}", response_model=schemas.Subscription, tags=["Subscriptions"])
def update_subscription(subscription_id: int, subscription: schemas.SubscriptionUpdate, db: Session = Depends(get_db)):
    logger.debug(f"Оновлення абонементу: id={subscription_id}, дані={subscription.dict()}")
    db_subscription = crud.update_subscription(db, subscription_id=subscription_id, subscription=subscription)
    if db_subscription is None:
        logger.warning(f"Абонемент не знайдений для оновлення: id={subscription_id}")
        raise HTTPException(status_code=404, detail="Subscription not found")
    logger.info(f"Абонемент оновлений: id={subscription_id}")
    return db_subscription


@app.delete("/subscriptions/{subscription_id}", response_model=schemas.Subscription, tags=["Subscriptions"])
def delete_subscription(subscription_id: int, db: Session = Depends(get_db)):
    logger.info(f"Видалення абонементу: id={subscription_id}")
    db_subscription = crud.delete_subscription(db, subscription_id=subscription_id)
    if db_subscription is None:
        logger.warning(f"Абонемент не знайдений для видалення: id={subscription_id}")
        raise HTTPException(status_code=404, detail="Subscription not found")
    logger.info(f"Абонемент видалений: id={subscription_id}")
    return db_subscription


@app.post("/workouts/", response_model=schemas.Workout, tags=["Workouts"])
def create_workout(workout: schemas.WorkoutCreate, db: Session = Depends(get_db)):
    logger.debug(f"Вхідні дані для створення тренування: {workout.dict()}")
    result = crud.create_workout(db=db, workout=workout)
    logger.info(f"Тренування створене: {result.id}")
    return result


@app.get("/workouts/", response_model=List[schemas.Workout], tags=["Workouts"])
def read_workouts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info(f"Запит на отримання тренувань: skip={skip}, limit={limit}")
    workouts = crud.get_workouts(db, skip=skip, limit=limit)
    logger.info(f"Повернуто {len(workouts)} тренувань")
    return workouts


@app.get("/workouts/{workout_id}", response_model=schemas.Workout, tags=["Workouts"])
def read_workout(workout_id: int, db: Session = Depends(get_db)):
    logger.info(f"Запит на отримання тренування: id={workout_id}")
    db_workout = crud.get_workout(db, workout_id=workout_id)
    if db_workout is None:
        logger.warning(f"Тренування не знайдене: id={workout_id}")
        raise HTTPException(status_code=404, detail="Workout not found")
    return db_workout


@app.put("/workouts/{workout_id}", response_model=schemas.Workout, tags=["Workouts"])
def update_workout(workout_id: int, workout: schemas.WorkoutUpdate, db: Session = Depends(get_db)):
    logger.debug(f"Оновлення тренування: id={workout_id}, дані={workout.dict()}")
    db_workout = crud.update_workout(db, workout_id=workout_id, workout=workout)
    if db_workout is None:
        logger.warning(f"Тренування не знайдене для оновлення: id={workout_id}")
        raise HTTPException(status_code=404, detail="Workout not found")
    logger.info(f"Тренування оновлене: id={workout_id}")
    return db_workout


@app.delete("/workouts/{workout_id}", response_model=schemas.Workout, tags=["Workouts"])
def delete_workout(workout_id: int, db: Session = Depends(get_db)):
    logger.info(f"Видалення тренування: id={workout_id}")
    db_workout = crud.delete_workout(db, workout_id=workout_id)
    if db_workout is None:
        logger.warning(f"Тренування не знайдене для видалення: id={workout_id}")
        raise HTTPException(status_code=404, detail="Workout not found")
    logger.info(f"Тренування видалене: id={workout_id}")
    return db_workout


@app.get("/clients/{client_id}/subscriptions/", response_model=List[schemas.Subscription], tags=["Clients"])
def read_client_subscriptions(client_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info(f"Запит на отримання абонементів клієнта: client_id={client_id}, skip={skip}, limit={limit}")
    db_client = crud.get_client(db, client_id=client_id)
    if db_client is None:
        logger.warning(f"Клієнт не знайдений: id={client_id}")
        raise HTTPException(status_code=404, detail="Client not found")
    subscriptions = crud.get_client_subscriptions(db, client_id=client_id, skip=skip, limit=limit)
    logger.info(f"Повернуто {len(subscriptions)} абонементів для клієнта: id={client_id}")
    return subscriptions


@app.get("/trainers/{trainer_id}/workouts/", response_model=List[schemas.Workout], tags=["Trainers"])
def read_trainer_workouts(trainer_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info(f"Запит на отримання тренувань тренера: trainer_id={trainer_id}, skip={skip}, limit={limit}")
    db_trainer = crud.get_trainer(db, trainer_id=trainer_id)
    if db_trainer is None:
        logger.warning(f"Тренер не знайдений: id={trainer_id}")
        raise HTTPException(status_code=404, detail="Trainer not found")
    workouts = crud.get_trainer_workouts(db, trainer_id=trainer_id, skip=skip, limit=limit)
    logger.info(f"Повернуто {len(workouts)} тренувань для тренера: id={trainer_id}")
    return workouts


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)