
from database.database import get_connection


class FoodRepository:

    def save(self, name, calories, protein,
             fats, carbohydrates, source="manual",
             usda_fdc_id=None, created_by=None):

        with get_connection() as connection:
            cursor = connection.execute("""
                INSERT INTO foods (
                    name, calories, protein,
                    carbs, fats, source,
                    usda_fdc_id, created_by
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                name, calories, protein,
                carbohydrates, fats, source,
                usda_fdc_id, created_by
            ))

            return cursor.lastrowid

    def get_by_id(self, food_id):
        with get_connection() as connection:
            connection.row_factory = __import__("sqlite3").Row

            result = connection.execute("""
                SELECT * FROM foods
                WHERE food_id = ?
            """, (food_id,)).fetchone()

            return dict(result) if result else None

    def get_all(self):
        with get_connection() as connection:
            connection.row_factory = __import__("sqlite3").Row

            results = connection.execute("""
                SELECT * FROM foods
                ORDER BY name
            """).fetchall()

            return [dict(row) for row in results]
