
import unittest

from domain.food import Food


class TestFoodDomain(unittest.TestCase):

    def setUp(self):
        self.valid_food = {
            "name": "Banana",
            "calories": 89,
            "protein": 1.09,
            "fats": 0.33,
            "carbohydrates": 22.84,
            "servings": 1
        }

    def test_create_valid_food(self):
        food = Food(**self.valid_food)

        self.assertEqual(food.name, "Banana")
        self.assertEqual(food.calories, 89)
        self.assertEqual(food.servings, 1)

    def test_food_name_cannot_be_empty(self):
        data = self.valid_food.copy()
        data["name"] = ""

        with self.assertRaises(ValueError):
            Food(**data)

    def test_food_name_cannot_be_whitespace(self):
        data = self.valid_food.copy()
        data["name"] = "   "

        with self.assertRaises(ValueError):
            Food(**data)

    def test_nutrition_cannot_be_negative(self):
        nutrients = [
            "calories",
            "protein",
            "fats",
            "carbohydrates"
        ]

        for nutrient in nutrients:
            with self.subTest(nutrient=nutrient):
                data = self.valid_food.copy()
                data[nutrient] = -10

                with self.assertRaises(ValueError):
                    Food(**data)

    def test_zero_nutrition_is_allowed(self):
        data = self.valid_food.copy()
        data["calories"] = 0
        data["protein"] = 0

        food = Food(**data)

        self.assertEqual(food.calories, 0)
        self.assertEqual(food.protein, 0)

    def test_food_requires_one_serving(self):
        data = self.valid_food.copy()
        data["servings"] = 0

        with self.assertRaisesRegex(
            ValueError,
            "Food must have at least one serving"
        ):
            Food(**data)

    def test_negative_servings_rejected(self):
        data = self.valid_food.copy()
        data["servings"] = -1

        with self.assertRaises(ValueError):
            Food(**data)

    def test_multiple_servings_allowed(self):
        data = self.valid_food.copy()
        data["servings"] = 2

        food = Food(**data)

        self.assertEqual(food.servings, 2)

    def test_nan_nutrition_rejected(self):
        data = self.valid_food.copy()
        data["calories"] = float("nan")

        with self.assertRaises(ValueError):
            Food(**data)


if __name__ == "__main__":
    unittest.main()
