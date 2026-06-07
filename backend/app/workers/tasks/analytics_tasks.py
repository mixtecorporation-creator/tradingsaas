from app.celery_app import celery_app


@celery_app.task(bind=True)
def update_performance_snapshots(self, user_id: str):
    """Recalculate and store performance snapshots for a user."""
    pass


@celery_app.task(bind=True)
def recalculate_leaderboards(self, period: str = "all_time"):
    """Recompute leaderboard rankings."""
    pass
