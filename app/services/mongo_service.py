from typing import Any, Optional

from pymongo.errors import PyMongoError
from pymongo.results import DeleteResult, InsertOneResult, UpdateResult

from app.config.settings import settings
from app.db.mongo import MongoConnection
from app.exceptions import (
    ObjectNotFoundException,
    OptimisticLockingException,
    PyMongoException,
)
from app.models.file_metadata import FileMetadata


class MongoService:
    """
    A service class for interacting with MongoDB to manage file metadata.
    """

    def __init__(self, mongo_connection: MongoConnection) -> None:
        self.mongo_connection = mongo_connection
        self.collection = self.mongo_connection.get_collection(
            settings.FM_MONGO_COLLECTION
        )

    def save_metadata(self, metadata: FileMetadata) -> str:
        """
        Save file metadata to the MongoDB collection.

        Args:
            metadata (FileMetadata): The metadata of the file to be saved.

        Returns:
            The inserted ID of the saved metadata document.
        """
        try:
            document: dict[str, Any] = metadata.model_dump()
            result: InsertOneResult = self.collection.insert_one(document)
        except PyMongoError:
            raise PyMongoException()
        else:
            return str(result.inserted_id)

    def get_metadata(self, file_id: str) -> Optional[dict[str, Any]]:
        """
        Retrieve file metadata from the MongoDB collection by file ID.

        Args:
            file_id (str): The ID of the file to retrieve metadata for.

        Returns:
            The metadata document if found, otherwise None.
        """
        try:
            metadata: Optional[dict[str, Any]] = self.collection.find_one(
                {"file_id": file_id}
            )
        except PyMongoError:
            raise PyMongoException()
        else:
            return metadata

    def delete_metadata(self, file_id: str) -> DeleteResult:
        """
        Remove file metadata from the MongoDB collection by file ID.

        Args:
            file_id (str): The ID of the file to remove metadata for.

        Returns:
            The result of the deletion operation.
        """
        try:
            result: DeleteResult = self.collection.delete_one({"file_id": file_id})
        except PyMongoError:
            raise PyMongoException()
        else:
            return result

    def update_metadata(
        self, file_id: str, update_fields: dict[str, Any]
    ) -> UpdateResult:
        """
        Update file metadata in the MongoDB collection by file ID using optimistic locking.

        Args:
            file_id (str): The ID of the file to update metadata for.
            update_fields (dict[str, Any]): The fields to update in the metadata document.

        Returns:
            The result of the update operation.
        """
        try:
            document = self.collection.find_one({"file_id": file_id})
            if not document:
                raise ObjectNotFoundException()

            current_version = document.get("version", 1)

            update = {"$set": update_fields, "$inc": {"version": 1}}

            result: UpdateResult = self.collection.update_one(
                {"file_id": file_id, "version": current_version}, update
            )

            if result.modified_count == 0:
                raise OptimisticLockingException()
        except PyMongoError:
            raise PyMongoException()
        return result
