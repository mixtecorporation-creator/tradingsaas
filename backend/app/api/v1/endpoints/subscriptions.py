from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.domains.subscriptions.schemas import (
    SubscriptionPlanResponse, CreateSubscriptionRequest,
    UserSubscriptionResponse, PaymentResponse, SubscriptionWithPlanResponse,
)
from app.domains.subscriptions.service import SubscriptionService

router = APIRouter()


@router.get("/plans", response_model=list[SubscriptionPlanResponse])
async def list_plans(db: AsyncSession = Depends(get_db)):
    service = SubscriptionService(db)
    plans = await service.list_plans()
    return [SubscriptionPlanResponse.model_validate(p).model_dump(mode="json") for p in plans]


@router.get("/plans/{plan_id}", response_model=SubscriptionPlanResponse)
async def get_plan(plan_id: str, db: AsyncSession = Depends(get_db)):
    service = SubscriptionService(db)
    plan = await service.get_plan(plan_id)
    return SubscriptionPlanResponse.model_validate(plan).model_dump(mode="json")


@router.get("/my")
async def my_subscription(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = SubscriptionService(db)
    sub = await service.get_my_subscription(user.id)
    if not sub:
        return None
    plan = await service.get_plan(str(sub.plan_id))
    return SubscriptionWithPlanResponse(
        id=sub.id, plan=SubscriptionPlanResponse.model_validate(plan).model_dump(mode="json"),
        status=sub.status, current_period_start=sub.current_period_start,
        current_period_end=sub.current_period_end, canceled_at=sub.canceled_at,
        created_at=sub.created_at,
    ).model_dump(mode="json")


@router.post("/subscribe", response_model=UserSubscriptionResponse, status_code=201)
async def subscribe(
    body: CreateSubscriptionRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = SubscriptionService(db)
    sub = await service.subscribe(user.id, body)
    return UserSubscriptionResponse.model_validate(sub).model_dump(mode="json")


@router.post("/cancel")
async def cancel_subscription(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = SubscriptionService(db)
    sub = await service.cancel_subscription(user.id)
    return {"message": "Subscription canceled", "status": sub.status}


@router.get("/payments", response_model=list[PaymentResponse])
async def list_payments(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = SubscriptionService(db)
    payments = await service.get_payments(user.id)
    return [PaymentResponse.model_validate(p).model_dump(mode="json") for p in payments]
