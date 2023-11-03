class ApiUserException(Exception):
    """
    Allows raising of errors that aren't internal to the application.
    """

    def __init__(self, message, status_code=400):
        self.status_code = status_code
        super().__init__(message)
