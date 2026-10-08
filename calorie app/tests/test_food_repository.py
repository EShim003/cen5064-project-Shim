
import unittest
import sqlite3
from unittest.mock import patch

from repository.food_repository import FoodRepository


class TestFoodRepository(unittest.TestCase):

    def setUp(self):
        self.db_uri = f"file:test_food_{id(self)}?mode=memory&cache=shared"

        self.connection = sqlite3.connect(
            self.db_uri,
            uri=True
        )

        self.connection.execute("""
            CREATE TABLE foods (
                food_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                calories REAL NOT NULL,
                protein REAL NOT NULL,
                carbs REAL NOT NULL,
                fats REAL NOT NULL,
                source TEXT NOT NULL,
                usda_fdc_id INTEGER,
                created_by INTEGER
            )
        """)
        self.connection.commit()

        self.patcher = patch(
            "repository.food_repository.get_connection",
            side_effect=self.get_test_connection
        )
        self.patcher.start()

        self.repository = FoodRepository()

   
    def get_test_connection(self):
        return sqlite3.connect(self.db_uri, uri=True)

    def tearDown(self):
        self.patcher.stop()
        self.connection.close()

    def test_save_manual_food(self):
        # Save a manually entered food
        food_id = self.repository.save(
            name="Peanut Butter",
            calories=588,
            protein=25,
            fats=50,
            carbohydrates=20,
            source="manual"
        )

        self.assertIsNotNone(food_id)

    def test_get_food_by_id(self):
        # Save a food
        food_id = self.repository.save(
            name="Banana",
            calories=89,
            protein=1.1,
            fats=0.3,
            carbohydrates=22.8,
            source="manual"
        )

        # Retrieve the saved food
        food = self.repository.get_by_id(food_id)

        self.assertEqual(food["name"], "Banana")
        self.assertEqual(food["calories"], 89)
        self.assertEqual(food["protein"], 1.1)

    def test_save_usda_food(self):
        # Save a food retrieved from USDA
        food_id = self.repository.save(
            name="Chicken Breast",
            calories=165,
            protein=31,
            fats=3.6,
            carbohydrates=0,
            source="usda",
            usda_fdc_id=123456
        )

        food = self.repository.get_by_id(food_id)

        self.assertEqual(food["source"], "usda")
        self.assertEqual(food["usda_fdc_id"], 123456)


if __name__ == "__main__":
    unittest.main()
