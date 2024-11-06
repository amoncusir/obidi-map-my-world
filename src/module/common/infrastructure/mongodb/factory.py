from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from src.config.mongodb import MongoDBSettings


def build_client(settings: MongoDBSettings) -> AsyncMongoClient:
    return AsyncMongoClient(settings.url)


def get_database(client: AsyncMongoClient, settings: MongoDBSettings) -> AsyncDatabase:
    if settings.database is None:
        return client.get_default_database()

    return client[settings.database]
