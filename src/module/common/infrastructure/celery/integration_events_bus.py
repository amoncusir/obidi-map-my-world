from dataclasses import dataclass

from celery import Celery
from celery.result import AsyncResult

from src.module.common.application.integration_events import IntegrationEvent
from src.module.common.application.integration_events_bus import (
    IntegrationEventsBus,
    IntegrationEventTask,
)


@dataclass
class CeleryIntegrationEventsBus(IntegrationEventsBus):

    celery: Celery

    async def async_trigger(self, event: IntegrationEvent) -> IntegrationEventTask:
        result: AsyncResult = self.celery.send_task(event.name(), args=[event.model_dump()])

        return IntegrationEventTask(id=result.task_id)
