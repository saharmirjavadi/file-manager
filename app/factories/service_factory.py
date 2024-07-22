from config.settings import Settings

from app.adapters.minio_adapter import MinioAdapter
from app.db.mongo import MongoConnection
from app.services.minio_client import MinioClient
from app.services.minio_service import MinioService
from app.services.mongo_service import MongoService


class ServiceFactory:
    @staticmethod
    def create_minio_service() -> MinioService:
        minio_client = MinioClient()
        minio_adapter = MinioAdapter(minio_client)
        return MinioService(minio_adapter)

    @staticmethod
    def create_mongo_service() -> MongoService:
        settings = Settings()
        mongo_connection = MongoConnection(settings)
        return MongoService(mongo_connection)
