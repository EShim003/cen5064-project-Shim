
class AuthController:

    def __init__(self, auth_service):
        self.auth_service = auth_service

    def register(self, username, email, password):
        """Register a new user."""
        return self.auth_service.register(
            username, email, password
        )

    def login(self, username, password):
        """Authenticate an existing user."""
        return self.auth_service.login(
            username, password
        )
