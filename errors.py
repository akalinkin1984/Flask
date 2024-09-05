class HttpError(Exception):

    def __init__(self, status_code: int, error_msg: str | dict | list):
        self.status_code = status_code
        self.error_msg = error_msg
