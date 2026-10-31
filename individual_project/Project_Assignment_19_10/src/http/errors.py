class HttpError(Exception):
    def __init__(self, status: int, reason: str = ""):
        self.status = status
        self.reason = reason
        super().__init__(f"HTTP {status} {reason}".strip())
