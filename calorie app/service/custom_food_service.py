
import math
from datetime import date

from domain.food_log import FoodLog


class CustomFoodService:
    """Handles manually entered food log entries."""

    def __init__(self, food_log_repository):
        self.food_log_repository = food_log_repository

    def add_custom_food(
        self,
        user_id,
        name,
        grams,
        calories,
        protein,
        carbohydrates,
        fats
    ):
        """Validate and save a custom food entry."""

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Food name cannot be empty.")

        values = {
            "grams": grams,
            "calories": calories,
            "protein": protein,
            "carbohydrates": carbohydrates,
            "fats": fats
        }

        for field, value in values.items():
            if (
                isinstance(value, bool)
                or not isinstance(value, (int, float))
                or not math.isfinite(value)
                or (value <= 0 if field == "grams" else value < 0)
            ):
                raise ValueError(
                    f"Invalid {field} value."
                )

        entry = FoodLog(
            user_id=user_id,
            food_name=name.strip(),
            grams=grams,
            calories=calories,
            protein=protein,
            carbohydrates=carbohydrates,
            fats=fats,
            logged_date=date.today().isoformat()
        )

        return self.food_log_repository.save(entry)
