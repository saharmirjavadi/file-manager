class OptimisticLockingException(Exception):
    def get_error_message(self) -> str:
        return "must have been updated in the meantime"

    def get_error_code(self) -> int:
        return 400704

    def get_http_status_code(self) -> int:
        return 500
