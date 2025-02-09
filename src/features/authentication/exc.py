class AuthenticationCommandError(Exception):
    ...


class UserNotFoundError(AuthenticationCommandError):
    def __init__(self):
        self.msg = "User with provided email doesn't exist"
        super().__init__(self.msg)
