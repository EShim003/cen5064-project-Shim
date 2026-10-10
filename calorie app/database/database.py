
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "calorie_tracker.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database():
    with get_connection() as connection:

        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS foods (
                food_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                calories REAL NOT NULL CHECK(calories >= 0),
                protein REAL NOT NULL CHECK(protein >= 0),
                carbs REAL NOT NULL CHECK(carbs >= 0),
                fats REAL NOT NULL CHECK(fats >= 0),
                source TEXT NOT NULL
                    CHECK(source IN ('manual', 'usda')),
                usda_fdc_id INTEGER,
                created_by INTEGER,
                FOREIGN KEY (created_by)
                    REFERENCES users(user_id)
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS food_logs (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                food_id INTEGER NOT NULL,
                grams REAL NOT NULL CHECK(grams > 0),
                date TEXT NOT NULL,
                FOREIGN KEY (user_id)
                    REFERENCES users(user_id),
                FOREIGN KEY (food_id)
                    REFERENCES foods(food_id)
            )
        """)

    print("Database initialized successfully!")
