class InvalidEnvironmentError(Exception):
    def __init__(self, environment: str) -> None:
        super().__init__(f"Unknow environment: {environment}")
