from celery import Celery

celery_app = Celery(
    "search_service",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/1",
    include=["src.main_service._celery.tasks"],
)

celery_app.conf.beat_schedule = {
    "sync_articles": {
        "task": "sync_articles",
        "schedule": 500,
    }
}
