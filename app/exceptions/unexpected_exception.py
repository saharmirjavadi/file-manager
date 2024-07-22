class UnexpectedException(Exception):
    def get_error_message(self) -> str:
        return "UnexpectedException"

    def get_error_code(self) -> int:
        return 400703

    def get_http_status_code(self) -> int:
        return 500
