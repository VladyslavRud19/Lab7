import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException

import models
import schemas
from database import engine, get_db


def get_client(db: Session, client_id: int):
    return db.query(models.Client).filter(models.Client.id == client_id).first()


def get_client_by_email(db: Session, email: str):
    return db.query(models.Client).filter(models.Client.email == email).first()


def get_clients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Client).offset(skip).limit(limit).all()


def create_client(db: Session, client: schemas.ClientCreate):
    db_client = models.Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


def update_client(db: Session, client_id: int, client: schemas.ClientUpdate):
    db_client = get_client(db, client_id)
    if db_client:
        update_data = client.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_client, key, value)
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
    return db_client


def delete_client(db: Session, client_id: int):
    db_client = get_client(db, client_id)
    if db_client:
        db.delete(db_client)
        db.commit()
    return db_client


def get_trainer(db: Session, trainer_id: int):
    return db.query(models.Trainer).filter(models.Trainer.id == trainer_id).first()


def get_trainer_by_email(db: Session, email: str):
    return db.query(models.Trainer).filter(models.Trainer.email == email).first()


def get_trainers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Trainer).offset(skip).limit(limit).all()


def create_trainer(db: Session, trainer: schemas.TrainerCreate):
    db_trainer = models.Trainer(**trainer.dict())
    db.add(db_trainer)
    db.commit()
    db.refresh(db_trainer)
    return db_trainer


def update_trainer(db: Session, trainer_id: int, trainer: schemas.TrainerUpdate):
    db_trainer = get_trainer(db, trainer_id)
    if db_trainer:
        update_data = trainer.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_trainer, key, value)
        db.add(db_trainer)
        db.commit()
        db.refresh(db_trainer)
    return db_trainer


def delete_trainer(db: Session, trainer_id: int):
    db_trainer = get_trainer(db, trainer_id)
    if db_trainer:
        db.delete(db_trainer)
        db.commit()
    return db_trainer


def get_subscription(db: Session, subscription_id: int):
    return db.query(models.Subscription).filter(models.Subscription.id == subscription_id).first()


def get_subscriptions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Subscription).offset(skip).limit(limit).all()


def get_client_subscriptions(db: Session, client_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Subscription)\
        .filter(models.Subscription.client_id == client_id)\
        .offset(skip).limit(limit).all()


def create_subscription(db: Session, subscription: schemas.SubscriptionCreate):
    # Перевірка на наявність активного абонементу
    active_subscriptions = db.query(models.Subscription)\
        .filter(models.Subscription.client_id == subscription.client_id)\
        .filter(models.Subscription.is_active == True).count()
    if active_subscriptions > 0:
        raise HTTPException(status_code=400, detail="Client already has an active subscription")
    db_subscription = models.Subscription(**subscription.dict())
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription


def update_subscription(db: Session, subscription_id: int, subscription: schemas.SubscriptionUpdate):
    db_subscription = get_subscription(db, subscription_id)
    if db_subscription:
        update_data = subscription.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_subscription, key, value)
        db.add(db_subscription)
        db.commit()
        db.refresh(db_subscription)
    return db_subscription


def delete_subscription(db: Session, subscription_id: int):
    db_subscription = get_subscription(db, subscription_id)
    if db_subscription:
        db.delete(db_subscription)
        db.commit()
    return db_subscription


def get_workout(db: Session, workout_id: int):
    return db.query(models.Workout).filter(models.Workout.id == workout_id).first()


def get_workouts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Workout).offset(skip).limit(limit).all()


def get_trainer_workouts(db: Session, trainer_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Workout)\
        .filter(models.Workout.trainer_id == trainer_id)\
        .offset(skip).limit(limit).all()


def create_workout(db: Session, workout: schemas.WorkoutCreate):
    db_workout = models.Workout(**workout.dict())
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout


def update_workout(db: Session, workout_id: int, workout: schemas.WorkoutUpdate):
    db_workout = get_workout(db, workout_id)
    if db_workout:
        update_data = workout.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_workout, key, value)
        db.add(db_workout)
        db.commit()
        db.refresh(db_workout)
    return db_workout


def delete_workout(db: Session, workout_id: int):
    db_workout = get_workout(db, workout_id)
    if db_workout:
        db.delete(db_workout)
        db.commit()
    return db_workout