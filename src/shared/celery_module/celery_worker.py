from celery import Celery


def get_celery_app():
    celery_inst = Celery("celery_service")
    celery_inst.config_from_object("src.shared.configs.celery_conf")
    celery_inst.autodiscover_tasks(packages=["src.shared.celery_module.tasks"])

    return celery_inst


celery_app = get_celery_app()
