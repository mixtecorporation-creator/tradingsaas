import uuid
from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.subscription import (
    SubscriptionPlan, UserSubscription, Payment, CreatorSubscription, Payout,
)


class SubscriptionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_plans(self) -> list[SubscriptionPlan]:
        result = await self.db.execute(
            select(SubscriptionPlan).where(SubscriptionPlan.active).order_by(SubscriptionPlan.price_monthly)
        )
        return list(result.scalars().all())

    async def find_plan(self, plan_id: uuid.UUID) -> SubscriptionPlan | None:
        result = await self.db.execute(select(SubscriptionPlan).where(SubscriptionPlan.id == plan_id))
        return result.scalar_one_or_none()

    async def find_user_subscription(self, user_id: uuid.UUID) -> UserSubscription | None:
        result = await self.db.execute(
            select(UserSubscription)
            .where(UserSubscription.user_id == user_id, UserSubscription.status == "active")
            .options(selectinload(UserSubscription.plan))
        )
        return result.scalar_one_or_none()

    async def create_subscription(self, user_id: uuid.UUID, plan_id: uuid.UUID, billing: str) -> UserSubscription:
        now = datetime.now(timezone.utc)
        days = 30 if billing == "monthly" else 365
        sub = UserSubscription(
            user_id=user_id,
            plan_id=plan_id,
            status="active",
            current_period_start=now,
            current_period_end=now.replace(day=min(now.day, 28)) + __import__("datetime").timedelta(days=days),
        )
        self.db.add(sub)
        await self.db.flush()
        return sub

    async def cancel_subscription(self, sub: UserSubscription) -> UserSubscription:
        sub.status = "canceled"
        sub.canceled_at = datetime.now(timezone.utc)
        self.db.add(sub)
        await self.db.flush()
        return sub

    async def get_payments(self, user_id: uuid.UUID) -> list[Payment]:
        result = await self.db.execute(
            select(Payment).where(Payment.user_id == user_id).order_by(Payment.created_at.desc()).limit(50)
        )
        return list(result.scalars().all())

    async def create_payment(self, user_id: uuid.UUID, sub_id: uuid.UUID | None, amount: Decimal) -> Payment:
        pmt = Payment(user_id=user_id, subscription_id=sub_id, amount=amount, currency="USD", status="completed", provider="stripe")
        self.db.add(pmt)
        await self.db.flush()
        return pmt
