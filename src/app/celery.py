from celery import Celery

from src.config.celery import CelerySettings


def build_celery(settings: CelerySettings) -> Celery:
    instance = Celery(
        "worker",
        include=[
            "src.module.recommendation.application.integration_event.handlers",
        ],
    )

    config = settings.model_dump()
    instance.conf.update(**config)

    return instance
