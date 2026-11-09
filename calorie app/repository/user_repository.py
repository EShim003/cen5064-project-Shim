
import sqlite3


class UserRepository:

    def __init__(self, db_path="calorie_tracker.db"):
        self.db_path = db_path
        self.create_table()

    def get_connection(self):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def create_table(self):
        """Create the users table if it does not exist."""

        with self.get_connection() as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    email TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL
                )
            """)

    def create_user(self, username, email, password_hash):
        """Save a new user in the database."""

        try:
            with self.get_connection() as connection:
                cursor = connection.execute(
                    """
                    INSERT INTO users (
                        username, email, password_hash
                    )
                    VALUES (?, ?, ?)
                    """,
                    (username, email, password_hash)
                )

                return cursor.lastrowid

        except sqlite3.IntegrityError:
            raise ValueError(
                "Username or email already exists."
            ) from None

    def get_by_username(self, username):
        """Find a user by username."""

        with self.get_connection() as connection:
            cursor = connection.execute(
                """
                SELECT id, username, email, password_hash
                FROM users
                WHERE username = ?
                """,
                (username,)
            )

            row = cursor.fetchone()
            return dict(row) if row else None

    def get_by_email(self, email):
        """Find a user by email."""

        with self.get_connection() as connection:
            cursor = connection.execute(
                """
                SELECT id, username, email, password_hash
                FROM users
                WHERE email = ?
                """,
                (email,)
            )

            row = cursor.fetchone()
            return dict(row) if row else None
