
from dataclasses import dataclass
import math


@dataclass
class Food:
    name: str
    calories: float
    protein: float
    fats: float
    carbohydrates: float
    servings: float = 1
    source: str = "manual"
    usda_fdc_id: int | None = None
    created_by: int | None = None
    food_id: int | None = None

    def __post_init__(self):
        # Food name must not be empty
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Food name cannot be empty")

        # Nutrition values cannot be negative
        nutrients = {
            "calories": self.calories,
            "protein": self.protein,
            "fats": self.fats,
            "carbohydrates": self.carbohydrates
        }

        for nutrient, value in nutrients.items():
            if (
                isinstance(value, bool)
                or not isinstance(value, (int, float))
                or not math.isfinite(value)
                or value < 0
            ):
                raise ValueError(
                    f"{nutrient} must be a finite non-negative number"
                )

        # Every food must have at least one serving
        if (
            isinstance(self.servings, bool)
            or not isinstance(self.servings, (int, float))
            or not math.isfinite(self.servings)
            or self.servings < 1
        ):
            raise ValueError(
                "Food must have at least one serving"
            )
