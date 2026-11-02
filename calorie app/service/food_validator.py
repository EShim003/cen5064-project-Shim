
class FoodValidator:

    @staticmethod
    def validate(name, calories, protein, fats, carbohydrates):

        if not name or not name.strip():
            raise ValueError("Food name cannot be empty")

        values = [calories, protein, fats, carbohydrates]

        if any(value < 0 for value in values):
            raise ValueError("Nutrition values cannot be negative")
