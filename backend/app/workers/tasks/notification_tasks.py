from app.celery_app import celery_app


@celery_app.task(bind=True)
def send_email_notification(self, user_id: str, subject: str, body: str):
    """Send an email notification."""
    pass
