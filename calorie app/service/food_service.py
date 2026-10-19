
class FoodService:

    def __init__(self, food_repository):
        self.food_repository = food_repository

    def add_food(self, name, calories, protein,
                 fats, carbohydrates, source="manual",
                 usda_fdc_id=None, created_by=None):

        if not name or not name.strip():
            raise ValueError("Food name cannot be empty")

        values = [calories, protein, fats, carbohydrates]

        if any(value < 0 for value in values):
            raise ValueError("Nutrition values cannot be negative")

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

    def calculate_macros(macros, grams):
    """Calculate nutrients for a specified weight in grams."""

    multiplier = grams / 100

    return {
        "calories": (
            macros["calories"] * multiplier
            if macros["calories"] is not None else None
        ),
        "protein": (
            macros["protein"] * multiplier
            if macros["protein"] is not None else None
        ),
        "carbohydrates": (
            macros["carbohydrates"] * multiplier
            if macros["carbohydrates"] is not None else None
        ),
        "fats": (
            macros["fats"] * multiplier
            if macros["fats"] is not None else None
        )
    }
