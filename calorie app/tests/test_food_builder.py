
import unittest

from domain.food_builder import FoodBuilder


class TestFoodBuilder(unittest.TestCase):

    def test_build_valid_food(self):
        food = (
            FoodBuilder()
            .set_name("Banana")
            .set_calories(89)
            .set_protein(1.09)
            .set_fats(0.33)
            .set_carbohydrates(22.84)
            .set_servings(1)
            .build()
        )

        self.assertEqual(food.name, "Banana")
        self.assertEqual(food.calories, 89)
        self.assertEqual(food.protein, 1.09)
        self.assertEqual(food.servings, 1)

    def test_builder_returns_self(self):
        builder = FoodBuilder()

        result = builder.set_name("Apple")

        self.assertIs(result, builder)

    def test_negative_calories_rejected(self):
        with self.assertRaises(ValueError):
            (
                FoodBuilder()
                .set_name("Invalid Food")
                .set_calories(-100)
                .set_protein(5)
                .set_fats(2)
                .set_carbohydrates(10)
                .build()
            )

    def test_zero_servings_rejected(self):
        with self.assertRaises(ValueError):
            (
                FoodBuilder()
                .set_name("Banana")
                .set_calories(89)
                .set_protein(1)
                .set_fats(0)
                .set_carbohydrates(23)
                .set_servings(0)
                .build()
            )

    def test_missing_name_rejected(self):
        with self.assertRaises(ValueError):
            (
                FoodBuilder()
                .set_calories(100)
                .set_protein(10)
                .set_fats(5)
                .set_carbohydrates(15)
                .build()
            )

    def test_default_values(self):
        food = (
            FoodBuilder()
            .set_name("Apple")
            .set_calories(52)
            .set_protein(0.3)
            .set_fats(0.2)
            .set_carbohydrates(14)
            .build()
        )

        self.assertEqual(food.servings, 1)
        self.assertEqual(food.source, "manual")


if __name__ == "__main__":
    unittest.main()
