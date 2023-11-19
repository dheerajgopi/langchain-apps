class NoApiKeyError(Exception):
    """
    Raised when API key is not provided.
    """

    def __init__(self, message='API key is not provided') -> None:
        super().__init__(message)


class NoIngredientsError(Exception):
    """
    Raised when no ingredients are provided.
    """

    def __init__(self, message='No ingredients are provided') -> None:
        super().__init__(message)