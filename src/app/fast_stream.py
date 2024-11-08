from logging import getLogger
from typing import List

from faststream.rabbit import (
    ExchangeType,
    RabbitBroker,
    RabbitExchange,
    RabbitQueue,
    RabbitRoute,
    RabbitRouter,
)

from src.config.fast_stream import FastStreamSettings
from src.module.common.application.event.integration import IntegrationEventSubscriber

logger = getLogger(__name__)


def build_router(exchange: RabbitExchange, subscribers: List[IntegrationEventSubscriber]) -> RabbitRouter:
    router = RabbitRouter(handlers=(build_route_handler(exchange, sub) for sub in subscribers))
    return router


def build_route_handler(exchange: RabbitExchange, subs: IntegrationEventSubscriber) -> RabbitRoute:
    queue_name = f"event.{subs.name()}"
    queue = RabbitQueue(queue_name, routing_key=subs.routing_key(), auto_delete=True)

    route = RabbitRoute(
        subs,
        queue,
        exchange=exchange,
        title=subs.__class__.__qualname__,
        description=subs.__class__.__doc__,
    )

    logger.debug(f"Added queue: %s for %s", queue_name, subs)

    return route


def build_broker(settings: FastStreamSettings, router: RabbitRouter) -> RabbitBroker:
    broker = RabbitBroker(**settings.model_dump())
    broker.include_router(router, include_in_schema=True)

    return broker


def build_exchange(settings: FastStreamSettings) -> RabbitExchange:
    return RabbitExchange(settings.exchange_name, ExchangeType.TOPIC, auto_delete=True)
