class NoApiKeyError(Exception):
    """
    Raised when API key is not provided.
    """

    def __init__(self, message='API key is not provided') -> None:
        super().__init__(message)