
from dataclasses import dataclass
from datetime import date
import math


@dataclass
class FoodLog:
    user_id: int
    food_name: str
    grams: float
    calories: float
    protein: float
    carbohydrates: float
    fats: float
    logged_date: str

    def __post_init__(self):
        if not isinstance(self.user_id, int) or isinstance(self.user_id, bool) or self.user_id <= 0:
            raise ValueError("A valid user ID is required.")

        if not isinstance(self.food_name, str) or not self.food_name.strip():
            raise ValueError("Food name cannot be empty.")

        values = {
            "grams": self.grams,
            "calories": self.calories,
            "protein": self.protein,
            "carbohydrates": self.carbohydrates,
            "fats": self.fats
        }

        for name, value in values.items():
            if (
                isinstance(value, bool)
                or not isinstance(value, (int, float))
                or not math.isfinite(value)
                or value < 0
            ):
                raise ValueError(f"Invalid {name} value.")

        if self.grams == 0:
            raise ValueError("Weight must be greater than zero.")

        date.fromisoformat(self.logged_date)
