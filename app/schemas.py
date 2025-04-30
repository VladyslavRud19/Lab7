from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, field_validator


class ClientBase(BaseModel):
    name: str
    email: str
    phone: str
    is_active: bool = True

    @field_validator('email')
    def email_must_contain_at(cls, v):
        if '@' not in v:
            raise ValueError('must contain @ symbol')
        return v


class ClientCreate(ClientBase):
    pass


class ClientUpdate(ClientBase):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None


class Client(ClientBase):
    id: int

    class Config:
        from_attributes = True


class TrainerBase(BaseModel):
    name: str
    email: str
    phone: str
    specialization: str

    @field_validator('email')
    def email_must_contain_at(cls, v):
        if '@' not in v:
            raise ValueError('must contain @ symbol')
        return v


class TrainerCreate(TrainerBase):
    pass


class TrainerUpdate(TrainerBase):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    specialization: Optional[str] = None


class Trainer(TrainerBase):
    id: int

    class Config:
        from_attributes = True


class SubscriptionBase(BaseModel):
    client_id: int
    subscription_type: str
    start_date: datetime
    end_date: datetime
    price: float
    is_active: bool = True


class SubscriptionCreate(SubscriptionBase):
    pass


class SubscriptionUpdate(SubscriptionBase):
    client_id: Optional[int] = None
    subscription_type: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    price: Optional[float] = None
    is_active: Optional[bool] = None


class Subscription(SubscriptionBase):
    id: int

    class Config:
        from_attributes = True


class WorkoutBase(BaseModel):
    name: str
    trainer_id: int
    workout_type: str
    start_time: datetime
    end_time: datetime
    max_participants: int


class WorkoutCreate(WorkoutBase):
    pass


class WorkoutUpdate(WorkoutBase):
    name: Optional[str] = None
    trainer_id: Optional[int] = None
    workout_type: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    max_participants: Optional[int] = None


class Workout(WorkoutBase):
    id: int

    class Config:
        from_attributes = True