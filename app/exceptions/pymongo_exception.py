class PyMongoException(Exception):
    def get_error_message(self) -> str:
        return "An unexpected error occurred"

    def get_error_code(self) -> int:
        return 400705

    def get_http_status_code(self) -> int:
        return 500
