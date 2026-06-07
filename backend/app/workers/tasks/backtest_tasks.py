from app.celery_app import celery_app


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def run_backtest(self, backtest_run_id: str):
    """Execute a backtest as a background task."""
    pass
