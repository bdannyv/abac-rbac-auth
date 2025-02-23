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
