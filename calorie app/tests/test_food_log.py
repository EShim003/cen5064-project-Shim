
import unittest
from unittest.mock import Mock
from datetime import date

from service.food_log_service import FoodLogService


class TestFoodLogService(unittest.TestCase):

    def setUp(self):
        self.repository = Mock()
        self.service = FoodLogService(self.repository)

        self.macros = {
            "name": "Banana",
            "calories": 89,
            "protein": 1.09,
            "carbohydrates": 22.84,
            "fats": 0.33
        }

    def test_add_food_to_log(self):
        self.repository.save.return_value = 1

        result = self.service.add_food(
            user_id=1,
            macros=self.macros,
            grams=150
        )

        self.assertEqual(result, 1)

        entry = self.repository.save.call_args.args[0]

        self.assertEqual(entry.user_id, 1)
        self.assertEqual(entry.food_name, "Banana")
        self.assertAlmostEqual(entry.calories, 133.5)
        self.assertAlmostEqual(entry.protein, 1.635)
        self.assertEqual(
            entry.logged_date,
            date.today().isoformat()
        )

    def test_calculate_daily_totals(self):
        self.repository.get_by_date.return_value = [
            {
                "calories": 100,
                "protein": 10,
                "carbohydrates": 20,
                "fats": 5
            },
            {
                "calories": 200,
                "protein": 20,
                "carbohydrates": 30,
                "fats": 10
            }
        ]

        totals = self.service.get_daily_totals(1)

        self.assertEqual(totals["calories"], 300)
        self.assertEqual(totals["protein"], 30)
        self.assertEqual(totals["carbohydrates"], 50)
        self.assertEqual(totals["fats"], 15)

    def test_empty_log_has_zero_totals(self):
        self.repository.get_by_date.return_value = []

        totals = self.service.get_daily_totals(1)

        self.assertEqual(totals["calories"], 0)
        self.assertEqual(totals["protein"], 0)
        self.assertEqual(totals["carbohydrates"], 0)
        self.assertEqual(totals["fats"], 0)

    def test_invalid_weight_rejected(self):
        with self.assertRaises(ValueError):
            self.service.add_food(1, self.macros, -50)

        self.repository.save.assert_not_called()

    def test_missing_nutrient_rejected(self):
        macros = self.macros.copy()
        macros["protein"] = None

        with self.assertRaises(ValueError):
            self.service.add_food(1, macros, 100)

        self.repository.save.assert_not_called()

    def test_log_is_scoped_to_user(self):
        self.repository.get_by_date.return_value = []

        self.service.get_daily_log(5, "2026-11-08")

        self.repository.get_by_date.assert_called_once_with(
            5, "2026-11-08"
        )

    def test_remove_food(self):
        self.repository.delete.return_value = True

        result = self.service.remove_food(10, 1)

        self.assertTrue(result)
        self.repository.delete.assert_called_once_with(
            10, 1
        )


if __name__ == "__main__":
    unittest.main()
