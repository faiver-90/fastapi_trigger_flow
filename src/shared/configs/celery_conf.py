# src/shared/configs/celery_conf.py
import os

from kombu import Exchange, Queue

# --- Брокер и бэкенд (можно через .env) ---
# Локальные вспомогательные переменные (НЕ в UPPERCASE!)
_broker_host  = os.getenv("RABBIT_HOST", "localhost")
_broker_user  = os.getenv("RABBIT_USER", "appuser")
_broker_pass  = os.getenv("RABBIT_PASS", "apppass")
_broker_vhost = os.getenv("RABBIT_VHOST", "appvhost")
broker_url = f"amqp://{_broker_user}:{_broker_pass}@{_broker_host}:5672/{_broker_vhost}"

result_backend = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")

# --- Сериализация/таймзона ---
task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
timezone = "UTC"
enable_utc = True

# --- Надёжность/поведение ---
task_acks_late = True
task_reject_on_worker_lost = True
task_acks_on_failure_or_timeout = True
broker_pool_limit = 10
broker_heartbeat = 30
broker_connection_retry_on_startup = True

# --- Exchanges и очереди ---
default_ex = Exchange("default", type="direct", durable=True)
notify_ex  = Exchange("notify",  type="direct", durable=True)

task_default_queue = "default"
task_queues = (
    Queue("default",       exchange=default_ex, routing_key="default",       durable=True),
    Queue("notify_email",  exchange=notify_ex,  routing_key="notify.email",  durable=True),
    Queue("notify_tg",     exchange=notify_ex,  routing_key="notify.tg",     durable=True),
    Queue("notify_sms",    exchange=notify_ex,  routing_key="notify.sms",    durable=True),
)

# --- Роутинг по имени задачи ---
task_routes = {
    "src.shared.celery_module.tasks.notify_email": {"queue": "notify_email", "routing_key": "notify.email"},
    "src.shared.celery_module.tasks.notify_tg":    {"queue": "notify_tg",    "routing_key": "notify.tg"},
    "src.shared.celery_module.tasks.notify_sms":   {"queue": "notify_sms",   "routing_key": "notify.sms"},
}

# --- Пример beat-расписания (опционально) ---
# beat_schedule = {
#     "cleanup-every-night": {
#         "task": "src.shared.celery_module.tasks.cleanup",
#         "schedule": crontab(hour=2, minute=0),
#     },
# }
