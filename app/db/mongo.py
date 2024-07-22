from config.settings import Settings
from pymongo import MongoClient


class MongoConnection:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def get_client(self) -> MongoClient:
        return MongoClient(
            self.settings.FM_MONGO_URI,
            username=self.settings.FM_MONGO_USER,
            password=self.settings.FM_MONGO_PASS,
        )

    def get_database(self) -> MongoClient:
        client = self.get_client()
        return client[self.settings.FM_MONGO_DB]

    def get_collection(self, collection_name: str) -> MongoClient:
        db = self.get_database()
        return db[collection_name]
