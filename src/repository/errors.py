class RepositoryError(Exception):
    # error class for repository errors
    def __init__(self, message):
        super().__init__(message)
        self.message = message
