
from argon2 import PasswordHasher
from argon2.exceptions import (
    VerifyMismatchError,
    VerificationError,
    InvalidHashError
)


class AuthService:

    def __init__(self, user_repository):
        self.user_repository = user_repository
        self.password_hasher = PasswordHasher()

    def register(self, username, email, password):
        """Create a new user account."""

        username = username.strip()
        email = email.strip()

        if not username or not email or not password:
            raise ValueError("All fields are required.")

        if len(password) < 8:
            raise ValueError(
                "Password must be at least 8 characters."
            )

        if self.user_repository.get_by_username(username):
            raise ValueError("Username already exists.")

        if self.user_repository.get_by_email(email):
            raise ValueError("Email already registered.")

        # Hash password before storing it
        password_hash = self.password_hasher.hash(password)

        # Save the new user
        user_id = self.user_repository.create_user(
            username,
            email,
            password_hash
        )

        return user_id

    def login(self, username, password):
        """Verify user credentials."""

        if not username or not password:
            return None

        user = self.user_repository.get_by_username(
            username.strip()
        )

        if user is None:
            return None

        try:
            self.password_hasher.verify(
                user["password_hash"],
                password
            )

            return user

        except (
            VerifyMismatchError,
            VerificationError,
            InvalidHashError
        ):
            return None
