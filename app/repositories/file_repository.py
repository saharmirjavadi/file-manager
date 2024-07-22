from app.models.file_metadata import FileMetadata
from app.services.mongo_service import MongoService


class FileRepository:
    def __init__(self, mongo_service: MongoService) -> None:
        self.mongo_service = mongo_service

    def save_metadata(self, metadata: FileMetadata) -> str:
        return self.mongo_service.save_metadata(metadata)

    def get_metadata(self, file_id: str) -> dict:
        return self.mongo_service.get_metadata(file_id)

    def delete_metadata(self, file_id: str) -> None:
        self.mongo_service.delete_metadata(file_id)

    def update_metadata(self, file_id: str, update_fields: dict) -> None:
        self.mongo_service.update_metadata(file_id, update_fields)
