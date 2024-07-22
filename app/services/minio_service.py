from typing import BinaryIO

from app.adapters.minio_adapter import MinioAdapter


class MinioService:
    def __init__(self, minio_adapter: MinioAdapter) -> None:
        self.minio_adapter = minio_adapter

    def store_temporary_file(
        self, file_extension: str, size: int, file_obj: BinaryIO
    ) -> tuple[str, str]:
        return self.minio_adapter.upload(file_extension, size, file_obj)

    def retrieve_file_content(self, file_id: str) -> bytes:
        return self.minio_adapter.download(file_id)

    def remove_file_and_metadata(self, file_id: str) -> None:
        self.minio_adapter.delete(file_id)

    def move_to_persistent_storage(self, file_id: str) -> None:
        self.minio_adapter.commit(file_id)

    def retrieve_file_info(self, file_name: str, bucket_name: str) -> dict:
        return self.minio_adapter.retrieve_info(file_name, bucket_name)
