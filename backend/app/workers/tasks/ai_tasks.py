from app.celery_app import celery_app


@celery_app.task(bind=True, max_retries=3, default_retry_delay=30)
def analyze_trade(self, analysis_id: str):
    """Run AI analysis on a trade."""
    pass
