class ObjectNotFoundException(Exception):
    def get_error_message(self) -> str:
        return "ObjectNotFoundException"

    def get_error_code(self) -> int:
        return 400701

    def get_http_status_code(self) -> int:
        return 404
