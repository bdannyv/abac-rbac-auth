class AuthenticationCommandError(Exception):
    ...


class UserNotFoundError(AuthenticationCommandError):
    def __init__(self):
        self.msg = "User with provided email doesn't exist"
        super().__init__(self.msg)


class EmailAlreadyExists(AuthenticationCommandError):
    def __init__(self):
        self.msg = "Email is already registered"
        super().__init__(self.msg)


class UnknownUserColumn(AuthenticationCommandError):
    def __init__(self):
        self.msg = "Used data do not correspond to application model"
        super().__init__(self.msg)
