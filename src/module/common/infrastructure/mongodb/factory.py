from typing import Optional

from pymongo import MongoClient
from pymongo.database import Database

from src.config.mongodb import MongoDBSettings


def build_client(settings: MongoDBSettings) -> MongoClient:
    return MongoClient(settings.url)


def get_database(client: MongoClient, settings: MongoDBSettings) -> Database:
    if settings.database is None:
        return client.get_default_database()

    return client[settings.database]
