class FileUploadException(Exception):
    def get_error_message(self) -> str:
        return "FileUploadException"

    def get_error_code(self) -> int:
        return 400702

    def get_http_status_code(self) -> int:
        return 400
