from typing import List

from faststream import FastStream
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


def build_app(broker: RabbitBroker) -> FastStream:
    app = FastStream(broker)
    yield app


def build_router(exchange: RabbitExchange, subscribers: List[IntegrationEventSubscriber]) -> RabbitRouter:
    router = RabbitRouter(handlers=(build_route_handler(exchange, sub) for sub in subscribers))
    return router


def build_route_handler(exchange: RabbitExchange, subs: IntegrationEventSubscriber) -> RabbitRoute:
    queue_name = f"event.{subs.routing_key()}"
    queue = RabbitQueue(queue_name, routing_key=subs.routing_key(), auto_delete=True)

    return RabbitRoute(
        subs,
        queue,
        exchange=exchange,
        title=subs.__class__.__qualname__,
        description=subs.__class__.__doc__,
    )


def build_broker(settings: FastStreamSettings, router: RabbitRouter) -> RabbitBroker:
    broker = RabbitBroker(**settings.model_dump())
    broker.include_router(router, include_in_schema=True)

    broker.connect()

    yield broker

    broker.close()


def build_exchange(settings: FastStreamSettings) -> RabbitExchange:
    return RabbitExchange(settings.exchange_name, ExchangeType.TOPIC, auto_delete=True)
