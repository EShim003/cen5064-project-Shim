

from domain.food_builder import FoodBuilder


class FoodService:

    def __init__(self, food_repository):
        self.food_repository = food_repository

    def add_food(
        self,
        name,
        calories,
        protein,
        fats,
        carbohydrates,
        source="manual",
        usda_fdc_id=None,
        created_by=None,
        servings=1
    ):
        # Construct the Food object using Builder
        food = (
            FoodBuilder()
            .set_name(name)
            .set_calories(calories)
            .set_protein(protein)
            .set_fats(fats)
            .set_carbohydrates(carbohydrates)
            .set_servings(servings)
            .set_source(source)
            .set_usda_fdc_id(usda_fdc_id)
            .set_created_by(created_by)
            .build()
        )

        # Save the validated Food object
        return self.food_repository.save(
            name=food.name,
            calories=food.calories,
            protein=food.protein,
            fats=food.fats,
            carbohydrates=food.carbohydrates,
            source=food.source,
            usda_fdc_id=food.usda_fdc_id,
            created_by=food.created_by
        )

    def get_food(self, food_id):
        return self.food_repository.get_by_id(food_id)

