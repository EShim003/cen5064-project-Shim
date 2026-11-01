
from service.food_validator import FoodValidator


class FoodService:

    def __init__(self, food_repository):
        self.food_repository = food_repository

    def add_food(self, name, calories, protein,
                 fats, carbohydrates, source="manual",
                 usda_fdc_id=None, created_by=None):

        FoodValidator.validate(
            name, calories, protein, fats, carbohydrates
        )

        return self.food_repository.save(
            name=name,
            calories=calories,
            protein=protein,
            fats=fats,
            carbohydrates=carbohydrates,
            source=source,
            usda_fdc_id=usda_fdc_id,
            created_by=created_by
        )

    def get_food(self, food_id):
        return self.food_repository.get_by_id(food_id)
