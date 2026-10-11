
import os
import requests
from dotenv import load_dotenv

load_dotenv()


class USDAFoodService:

    BASE_URL = "https://api.nal.usda.gov/fdc/v1"

    def __init__(self):
        self.api_key = os.getenv("USDA_API_KEY")

        if not self.api_key:
            raise ValueError("USDA_API_KEY is not configured")

    def search_food(self, food_name):
        """Search USDA for foods matching a name."""

        url = f"{self.BASE_URL}/foods/search"

        params = {
            "api_key": self.api_key,
            "query": food_name,
            "pageSize": 10,
            "dataType": ["Foundation", "SR Legacy"]
        }

        response = requests.get(
            url,
            params=params,
            timeout=15
        )
        response.raise_for_status()

        data = response.json()
        return data.get("foods", [])

    def get_food_details(self, fdc_id):
        """Retrieve complete nutrition data for a food."""

        url = f"{self.BASE_URL}/food/{fdc_id}"

        response = requests.get(
            url,
            params={"api_key": self.api_key},
            timeout=15
        )
        response.raise_for_status()

        return response.json()

    def get_macros(self, fdc_id):
        """Get nutrition values per 100 grams."""

        food = self.get_food_details(fdc_id)

        nutrients = food.get("foodNutrients", [])

        macros = {
            "name": food.get("description"),
            "calories": None,
            "protein": None,
            "carbohydrates": None,
            "fats": None
        }

        nutrient_ids = {
            1008: "calories",
            1003: "protein",
            1005: "carbohydrates",
            1004: "fats"
        }

        for item in nutrients:
            nutrient = item.get("nutrient", {})
            nutrient_id = nutrient.get("id")

            if nutrient_id in nutrient_ids:
                key = nutrient_ids[nutrient_id]
                macros[key] = item.get("amount")

        # Some foods use newer energy nutrient IDs
        if macros["calories"] is None:
            for item in nutrients:
                nutrient = item.get("nutrient", {})
                if nutrient.get("id") in (2047, 2048):
                    macros["calories"] = item.get("amount")
                    break

        return macros

