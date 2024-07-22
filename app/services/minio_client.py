import uuid
from contextlib import contextmanager
from typing import BinaryIO, Optional

from minio import Minio
from minio.commonconfig import CopySource
from minio.error import S3Error

from app.config.settings import Settings

from ..exceptions import (
    ObjectNotFoundException,
)
from .mongo_service import MongoService


class MinioClient:
    """
    A client class for interacting with MinIO storage.
    """

    def __init__(
        self,
        settings: Optional[Settings] = None,
        minio_client: Optional[Minio] = None,
        mongo_service: Optional[MongoService] = None,
    ) -> None:
        self.settings = settings or Settings()
        self.mongo_service = mongo_service or MongoService()
        self.minio_client = minio_client or self._create_minio_client()
        self._ensure_buckets_exist_and_create_if_needed()

    def _create_minio_client(self) -> Minio:
        return Minio(
            f"{self.settings.FM_STORAGE_HOST}:{self.settings.FM_STORAGE_PORT}",
            access_key=self.settings.FM_STORAGE_ACCESS_KEY,
            secret_key=self.settings.FM_STORAGE_SECRET_KEY,
            secure=False,
        )

    def _ensure_buckets_exist_and_create_if_needed(self) -> None:
        self._ensure_bucket_exists(self.settings.FM_TEMP_BUCKET)
        self._ensure_bucket_exists(self.settings.FM_PERSIST_BUCKET)

    def _ensure_bucket_exists(self, bucket_name: str) -> None:
        if not self.minio_client.bucket_exists(bucket_name):
            self.minio_client.make_bucket(bucket_name)

    @contextmanager
    def _handle_minio_errors(self):
        try:
            yield
        except S3Error as e:
            raise Exception(str(e))

    def store_temporary_file(
        self, file_extension: str, size: int, file_obj: BinaryIO
    ) -> tuple[Optional[str], Optional[str]]:
        file_id = uuid.uuid4().hex
        with self._handle_minio_errors():
            self.minio_client.put_object(
                bucket_name=self.settings.FM_TEMP_BUCKET,
                object_name=f"{file_id}{file_extension}",
                data=file_obj,
                length=size,
            )
        return file_id

    def retrieve_file_content(self, file_id: str) -> bytes | str:
        metadata = self._fetch_metadata_and_handle_error(file_id)
        file_extension = metadata["file_extension"]
        file_name = f"{file_id}{file_extension}"
        with self._handle_minio_errors():
            response = self.minio_client.get_object(
                metadata["bucket"],
                file_name,
            )
        return response.read()

    def remove_file_and_metadata(self, file_id: str) -> str | str:
        metadata = self._fetch_metadata_and_handle_error(file_id)
        file_extension = metadata["file_extension"]
        file_name = f"{file_id}{file_extension}"
        with self._handle_minio_errors():
            self.minio_client.remove_object(metadata["bucket"], file_name)
            self.mongo_service.delete_metadata(file_id)
        return file_id

    def move_to_persistent_storage(self, file_id: str) -> str | str:
        metadata = self._fetch_metadata_and_handle_error(file_id)
        file_extension = metadata["file_extension"]
        file_name = f"{file_id}{file_extension}"
        copy_source = CopySource(metadata["bucket"], file_name)
        with self._handle_minio_errors():
            self.minio_client.copy_object(
                self.settings.FM_TEMP_BUCKET, file_name, copy_source
            )
            self.get_file_metadata(file_name, self.settings.FM_TEMP_BUCKET)
            self.minio_client.remove_object(metadata["bucket"], file_name)
            update_fields = {
                "is_committed": True,
                "bucket": self.settings.FM_TEMP_BUCKET,
            }
            self.mongo_service.update_metadata(file_id, update_fields)
        return file_id
    
    def get_file_metadata(self, file_name: str, bucket_name: str) -> dict | str:
        with self._handle_minio_errors():
            return self.minio_client.stat_object(bucket_name, file_name)

    def _fetch_metadata_and_handle_error(self, file_id: str) -> dict:
        metadata = self.mongo_service.get_metadata(file_id)
        if not metadata:
            raise ObjectNotFoundException()
        return metadata
