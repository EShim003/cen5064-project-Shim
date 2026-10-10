# controller/add_food_controller.py

class AddFoodController:
    def __init__(self, food_service):
        self.food_service = food_service

    def add_food(self, name, calories, protein, fats, carbohydrates):
        """
        Handles a request to add a food and passes the
        food information to the FoodService.
        """

        if not name or not name.strip():
            raise ValueError("Food name is required")

        if calories < 0:
            raise ValueError("Calories cannot be negative")

        if protein < 0:
            raise ValueError("Protein cannot be negative")

        if fats < 0:
            raise ValueError("Fats cannot be negative")

        if carbohydrates < 0:
            raise ValueError("Carbohydrates cannot be negative")

        return self.food_service.add_food(
            name=name.strip(),
            calories=calories,
            protein=protein,
            fats=fats,
            carbohydrates=carbohydrates
        )

    # tests/test_add_food_controller.py

import unittest
from unittest.mock import Mock

from controller.add_food_controller import AddFoodController


