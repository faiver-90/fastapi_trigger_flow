import asyncio

from celery import shared_task

from src.modules.notifications.types.notifications_types_registry import (
    NOTIFY_REGISTRY,
)


@shared_task(name="sync_articles")
def sync_articles():
    print("Syncing articles...")


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=3, max_retries=5)
def notify_email(self, payload: dict, notif_config: dict | None = None):
    notifier = NOTIFY_REGISTRY.get("email")
    if not notifier:
        return {"status": "skip", "reason": "notifier_not_found"}
    return asyncio.run(notifier.send(payload, notif_config or {}))


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=3, max_retries=5)
def notify_tg(self, payload: dict, notif_config: dict | None = None):
    notifier = NOTIFY_REGISTRY.get("tg")
    if not notifier:
        return {"status": "skip", "reason": "notifier_not_found"}
    return asyncio.run(notifier.send(payload, notif_config or {}))


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=3, max_retries=5)
def notify_sms(self, payload: dict, notif_config: dict | None = None):
    notifier = NOTIFY_REGISTRY.get("sms")
    if not notifier:
        return {"status": "skip", "reason": "notifier_not_found"}
    return asyncio.run(notifier.send(payload, notif_config or {}))
