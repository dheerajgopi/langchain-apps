class NoApiKeyError(Exception):
    """
    Raised when API key is not provided.
    """

    def __init__(self, message='API key is not provided') -> None:
        super().__init__(message)


class NoTxtDocUploadedError(Exception):
    """
    Raised when uploaded text document is not provided.
    """

    def __init__(self, message='Please upload the text document') -> None:
        super().__init__(message)
