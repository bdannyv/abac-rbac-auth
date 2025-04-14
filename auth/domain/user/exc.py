class DomainException(Exception):
    ...


class InfraException(Exception):
    ...


class EmailAlreadyExists(DomainException):
    def __init__(self, email: str):
        self.message = f"Email {email} is already registered"
        super().__init__(self.message)


class ConcurrencyError(InfraException):
    pass
