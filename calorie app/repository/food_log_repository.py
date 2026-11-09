
import sqlite3


class FoodLogRepository:

    def __init__(self, db_path="calorie_tracker.db"):
        self.db_path = db_path
        self.create_table()

    def get_connection(self):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def create_table(self):
        with self.get_connection() as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS food_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    food_name TEXT NOT NULL,
                    grams REAL NOT NULL,
                    calories REAL NOT NULL,
                    protein REAL NOT NULL,
                    carbohydrates REAL NOT NULL,
                    fats REAL NOT NULL,
                    logged_date TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """)

    def save(self, entry):
        with self.get_connection() as connection:
            cursor = connection.execute("""
                INSERT INTO food_logs (
                    user_id, food_name, grams,
                    calories, protein, carbohydrates,
                    fats, logged_date
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                entry.user_id,
                entry.food_name,
                entry.grams,
                entry.calories,
                entry.protein,
                entry.carbohydrates,
                entry.fats,
                entry.logged_date
            ))

            return cursor.lastrowid

    def get_by_date(self, user_id, logged_date):
        with self.get_connection() as connection:
            rows = connection.execute("""
                SELECT *
                FROM food_logs
                WHERE user_id = ? AND logged_date = ?
                ORDER BY id
            """, (user_id, logged_date)).fetchall()

            return [dict(row) for row in rows]

    def delete(self, entry_id, user_id):
        with self.get_connection() as connection:
            cursor = connection.execute("""
                DELETE FROM food_logs
                WHERE id = ? AND user_id = ?
            """, (entry_id, user_id))

            return cursor.rowcount > 0
