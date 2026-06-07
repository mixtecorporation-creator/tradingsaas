import uuid
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.subscriptions.repository import SubscriptionRepository
from app.exceptions import NotFoundException, ConflictException


class SubscriptionService:
    def __init__(self, db: AsyncSession):
        self.repo = SubscriptionRepository(db)

    async def list_plans(self):
        return await self.repo.list_plans()

    async def get_plan(self, plan_id: str):
        plan = await self.repo.find_plan(uuid.UUID(plan_id))
        if not plan:
            raise NotFoundException("Plan not found")
        return plan

    async def get_my_subscription(self, user_id: uuid.UUID):
        return await self.repo.find_user_subscription(user_id)

    async def subscribe(self, user_id: uuid.UUID, data):
        plan_id = uuid.UUID(data.plan_id)
        plan = await self.repo.find_plan(plan_id)
        if not plan:
            raise NotFoundException("Plan not found")

        existing = await self.repo.find_user_subscription(user_id)
        if existing:
            raise ConflictException("Already subscribed to a plan")

        sub = await self.repo.create_subscription(user_id, plan_id, data.billing)
        price = plan.price_monthly if data.billing == "monthly" else plan.price_yearly
        await self.repo.create_payment(user_id, sub.id, price)
        return sub

    async def cancel_subscription(self, user_id: uuid.UUID):
        sub = await self.repo.find_user_subscription(user_id)
        if not sub:
            raise NotFoundException("No active subscription")
        return await self.repo.cancel_subscription(sub)

    async def get_payments(self, user_id: uuid.UUID):
        return await self.repo.get_payments(user_id)
