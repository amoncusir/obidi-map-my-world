from faststream import FastStream
from faststream.rabbit import ExchangeType, RabbitBroker, RabbitExchange, RabbitRouter

from src.config.fast_stream import FastStreamSettings


def build_app(broker: RabbitBroker) -> FastStream:
    return FastStream(broker)


def build_broker(settings: FastStreamSettings, router: RabbitRouter) -> RabbitBroker:
    broker = RabbitBroker(**settings.model_dump())
    broker.include_router(router, include_in_schema=True)
    return broker


def build_exchange(exchange_name: str) -> RabbitExchange:
    return RabbitExchange(exchange_name, ExchangeType.TOPIC, auto_delete=True)
