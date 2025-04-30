from sqlalchemy import Boolean, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    is_active = Column(Boolean, default=True)

    subscriptions = relationship("Subscription", back_populates="client")


class Trainer(Base):
    __tablename__ = "trainers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    specialization = Column(String)

    workouts = relationship("Workout", back_populates="trainer")


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    subscription_type = Column(String)  # monthly, yearly, etc.
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    price = Column(Float)
    is_active = Column(Boolean, default=True)

    client = relationship("Client", back_populates="subscriptions")


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    trainer_id = Column(Integer, ForeignKey("trainers.id"))
    workout_type = Column(String)  # yoga, pilates, etc.
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    max_participants = Column(Integer)

    trainer = relationship("Trainer", back_populates="workouts")