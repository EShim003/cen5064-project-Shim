
from domain.food import Food


class FoodBuilder:

    def __init__(self):
        self._data = {
            "name": None,
            "calories": None,
            "protein": None,
            "fats": None,
            "carbohydrates": None,
            "servings": 1,
            "source": "manual",
            "usda_fdc_id": None,
            "created_by": None
        }

    def set_name(self, name):
        self._data["name"] = name
        return self

    def set_calories(self, calories):
        self._data["calories"] = calories
        return self

    def set_protein(self, protein):
        self._data["protein"] = protein
        return self

    def set_fats(self, fats):
        self._data["fats"] = fats
        return self

    def set_carbohydrates(self, carbohydrates):
        self._data["carbohydrates"] = carbohydrates
        return self

    def set_servings(self, servings):
        self._data["servings"] = servings
        return self

    def set_source(self, source):
        self._data["source"] = source
        return self

    def set_usda_fdc_id(self, fdc_id):
        self._data["usda_fdc_id"] = fdc_id
        return self

    def set_created_by(self, user_id):
        self._data["created_by"] = user_id
        return self

    def build(self):
        """Construct a validated Food object."""
        return Food(**self._data)
