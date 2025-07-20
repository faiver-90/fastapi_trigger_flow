from celery.schedules import crontab

broker_url = "redis://redis:6379/0"
result_backend = "redis://redis:6379/1"
task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
timezone = "UTC"
enable_utc = True

beat_schedule = {
    "sync-articles-every-5-min": {
        "task": "sync_articles",
        "schedule": crontab(minute="*"),
    },
}
