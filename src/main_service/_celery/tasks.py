from src.main_service._celery.celery_worker import celery_app


@celery_app.task(name="sync_articles")
def sync_articles():
    print("Syncing articles...")
