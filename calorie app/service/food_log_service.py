
from datetime import date

from domain.food_log import FoodLog
from service.macro_calculator import MacroCalculator


class FoodLogService:

    def __init__(self, food_log_repository):
        self.repository = food_log_repository

    def add_food(self, user_id, macros, grams):
        # Validate weight before calculation
        import math

        if (
            isinstance(grams, bool)
            or not isinstance(grams, (int, float))
            or not math.isfinite(grams)
            or grams <= 0
        ):
            raise ValueError("Weight must be positive and finite.")

        # Calculate nutrients for the selected grams
        result = MacroCalculator.calculate(macros, grams)

        # Some USDA nutrients may be missing.
        # Require complete data before recording totals.
        if any(value is None for value in result.values()):
            raise ValueError(
                "Cannot log food with missing nutrient values."
            )

        entry = FoodLog(
            user_id=user_id,
            food_name=macros["name"],
            grams=grams,
            calories=result["calories"],
            protein=result["protein"],
            carbohydrates=result["carbohydrates"],
            fats=result["fats"],
            logged_date=date.today().isoformat()
        )

        return self.repository.save(entry)

    def get_daily_log(self, user_id, logged_date=None):
        if logged_date is None:
            logged_date = date.today().isoformat()

        return self.repository.get_by_date(
            user_id, logged_date
        )

    def get_daily_totals(self, user_id, logged_date=None):
        entries = self.get_daily_log(user_id, logged_date)

        totals = {
            "calories": 0.0,
            "protein": 0.0,
            "carbohydrates": 0.0,
            "fats": 0.0
        }

        for entry in entries:
            for nutrient in totals:
                totals[nutrient] += entry[nutrient]

        return totals

    def remove_food(self, entry_id, user_id):
        return self.repository.delete(entry_id, user_id)
