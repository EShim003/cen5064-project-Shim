import unittest
from unittest.mock import Mock
from controller.add_food_controller import AddFoodController

class TestAddFoodController(unittest.TestCase):

    def setUp(self):
        self.food_service = Mock()
        self.controller = AddFoodController(self.food_service)

    def test_add_food_successfully(self):
        self.food_service.add_food.return_value = True

        result = self.controller.add_food(
            name="Chicken",
            calories=200,
            protein=30,
            fats=5,
            carbohydrates=10
        )

        self.food_service.add_food.assert_called_once_with(
            name="Chicken",
            calories=200,
            protein=30,
            fats=5,
            carbohydrates=10
        )

        self.assertTrue(result)

    def test_add_food_invalid_calories(self):
        with self.assertRaises(ValueError):
            self.controller.add_food(
                name="Chicken",
                calories=-200,
                protein=30,
                fats=5,
                carbohydrates=10
            )

        self.food_service.add_food.assert_not_called()


if __name__ == "__main__":
    unittest.main()