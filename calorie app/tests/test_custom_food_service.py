
import unittest
from unittest.mock import Mock
from datetime import date

from service.custom_food_service import CustomFoodService


class TestCustomFoodService(unittest.TestCase):

    def setUp(self):
        """Create a mock repository and service for each test."""
        self.mock_repository = Mock()
        self.custom_food_service = CustomFoodService(
            self.mock_repository
        )

        self.valid_food = {
            "user_id": 1,
            "name": "Homemade Protein Pancakes",
            "grams": 150,
            "calories": 300,
            "protein": 25,
            "carbohydrates": 35,
            "fats": 8
        }

    def test_add_custom_food_successfully(self):
        """Test that a user can add a custom food."""

        self.mock_repository.save.return_value = 1

        result = self.custom_food_service.add_custom_food(
            **self.valid_food
        )

        self.assertEqual(result, 1)
        self.mock_repository.save.assert_called_once()

        saved_food = self.mock_repository.save.call_args.args[0]

        self.assertEqual(
            saved_food.food_name,
            "Homemade Protein Pancakes"
        )
        self.assertEqual(saved_food.user_id, 1)
        self.assertEqual(saved_food.grams, 150)

    def test_custom_food_calories_and_macros(self):
        """Test that calories and macros are saved correctly."""

        self.custom_food_service.add_custom_food(
            **self.valid_food
        )

        saved_food = self.mock_repository.save.call_args.args[0]

        self.assertEqual(saved_food.calories, 300)
        self.assertEqual(saved_food.protein, 25)
        self.assertEqual(saved_food.carbohydrates, 35)
        self.assertEqual(saved_food.fats, 8)

    def test_custom_food_uses_current_date(self):
        """Test that custom food is logged for today's date."""

        self.custom_food_service.add_custom_food(
            **self.valid_food
        )

        saved_food = self.mock_repository.save.call_args.args[0]

        self.assertEqual(
            saved_food.logged_date,
            date.today().isoformat()
        )

    def test_empty_food_name(self):
        """Test that a food cannot have an empty name."""

        invalid_food = self.valid_food.copy()
        invalid_food["name"] = ""

        with self.assertRaises(ValueError):
            self.custom_food_service.add_custom_food(
                **invalid_food
            )

        self.mock_repository.save.assert_not_called()

    def test_whitespace_food_name(self):
        """Test that whitespace-only food names are rejected."""

        invalid_food = self.valid_food.copy()
        invalid_food["name"] = "   "

        with self.assertRaises(ValueError):
            self.custom_food_service.add_custom_food(
                **invalid_food
            )

        self.mock_repository.save.assert_not_called()

    def test_negative_calories(self):
        """Test that negative calories are rejected."""

        invalid_food = self.valid_food.copy()
        invalid_food["calories"] = -100

        with self.assertRaises(ValueError):
            self.custom_food_service.add_custom_food(
                **invalid_food
            )

        self.mock_repository.save.assert_not_called()

    def test_negative_macronutrients(self):
        """Test that negative macronutrients are rejected."""

        for nutrient in [
            "protein",
            "carbohydrates",
            "fats"
        ]:
            with self.subTest(nutrient=nutrient):
                self.mock_repository.reset_mock()

                invalid_food = self.valid_food.copy()
                invalid_food[nutrient] = -5

                with self.assertRaises(ValueError):
                    self.custom_food_service.add_custom_food(
                        **invalid_food
                    )

                self.mock_repository.save.assert_not_called()

    def test_zero_grams(self):
        """Test that food weight must be greater than zero."""

        invalid_food = self.valid_food.copy()
        invalid_food["grams"] = 0

        with self.assertRaises(ValueError):
            self.custom_food_service.add_custom_food(
                **invalid_food
            )

        self.mock_repository.save.assert_not_called()

    def test_negative_grams(self):
        """Test that negative food weights are rejected."""

        invalid_food = self.valid_food.copy()
        invalid_food["grams"] = -50

        with self.assertRaises(ValueError):
            self.custom_food_service.add_custom_food(
                **invalid_food
            )

        self.mock_repository.save.assert_not_called()

    def test_zero_macronutrients_allowed(self):
        """Test that zero macronutrients are valid."""

        food = self.valid_food.copy()
        food["protein"] = 0
        food["carbohydrates"] = 0
        food["fats"] = 0

        self.custom_food_service.add_custom_food(
            **food
        )

        self.mock_repository.save.assert_called_once()

        saved_food = self.mock_repository.save.call_args.args[0]

        self.assertEqual(saved_food.protein, 0)
        self.assertEqual(saved_food.carbohydrates, 0)
        self.assertEqual(saved_food.fats, 0)

    def test_invalid_numeric_values(self):
        """Test that NaN and infinity are rejected."""

        invalid_values = [
            float("nan"),
            float("inf"),
            float("-inf")
        ]

        for field in [
            "grams",
            "calories",
            "protein",
            "carbohydrates",
            "fats"
        ]:
            for value in invalid_values:
                with self.subTest(field=field, value=value):
                    self.mock_repository.reset_mock()

                    invalid_food = self.valid_food.copy()
                    invalid_food[field] = value

                    with self.assertRaises(ValueError):
                        self.custom_food_service.add_custom_food(
                            **invalid_food
                        )

                    self.mock_repository.save.assert_not_called()

    def test_food_name_is_trimmed(self):
        """Test that extra spaces are removed from food names."""

        food = self.valid_food.copy()
        food["name"] = "  Homemade Protein Pancakes  "

        self.custom_food_service.add_custom_food(
            **food
        )

        saved_food = self.mock_repository.save.call_args.args[0]

        self.assertEqual(
            saved_food.food_name,
            "Homemade Protein Pancakes"
        )


if __name__ == "__main__":
    unittest.main()
