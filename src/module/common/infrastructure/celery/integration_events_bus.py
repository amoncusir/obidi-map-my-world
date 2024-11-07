from src.module.common.application.integration_events import IntegrationEvent
from src.module.common.application.integration_events_bus import IntegrationEventsBus


class CeleryIntegrationEventsBus(IntegrationEventsBus):

    async def async_trigger(self, event: IntegrationEvent): ...
