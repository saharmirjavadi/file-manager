from typing import BinaryIO

from app.services.minio_client import MinioClient


class MinioAdapter:
    def __init__(self, minio_client: MinioClient) -> None:
        self.minio_client = minio_client

    def upload(
        self, file_extension: str, size: int, file_obj: BinaryIO
    ) -> tuple[str, str]:
        return self.minio_client.store_temporary_file(file_extension, size, file_obj)

    def download(self, file_id: str) -> bytes:
        return self.minio_client.retrieve_file_content(file_id)

    def delete(self, file_id: str) -> None:
        self.minio_client.remove_file_and_metadata(file_id)

    def commit(self, file_id: str) -> None:
        self.minio_client.move_to_persistent_storage(file_id)

    def retrieve_info(self, file_name: str, bucket_name: str) -> dict:
        return self.minio_client.get_file_metadata(file_name, bucket_name)
