import uuid
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel


class SubscriptionPlanResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None = None
    price_monthly: Decimal
    price_yearly: Decimal
    features: dict = {}
    active: bool = True

    model_config = {"from_attributes": True}


class CreateSubscriptionRequest(BaseModel):
    plan_id: str
    billing: str = "monthly"


class UserSubscriptionResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    plan_id: uuid.UUID
    status: str
    current_period_start: datetime
    current_period_end: datetime
    created_at: datetime
    canceled_at: datetime | None = None

    model_config = {"from_attributes": True}


class PaymentResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    amount: Decimal
    currency: str
    status: str
    provider: str
    created_at: datetime

    model_config = {"from_attributes": True}


class CreatorSubscriptionResponse(BaseModel):
    id: uuid.UUID
    creator_id: uuid.UUID
    subscriber_id: uuid.UUID
    tier: str
    price: Decimal
    status: str
    current_period_end: datetime

    model_config = {"from_attributes": True}


class SubscriptionWithPlanResponse(BaseModel):
    id: uuid.UUID
    plan: SubscriptionPlanResponse
    status: str
    current_period_start: datetime
    current_period_end: datetime
    canceled_at: datetime | None = None
    created_at: datetime
