
import os
import requests


class USDAFoodService:

    BASE_URL = "https://api.nal.usda.gov/fdc/v1"

    def __init__(self):
        self.api_key = os.getenv("USDA_API_KEY")

        if not self.api_key:
            raise ValueError("USDA_API_KEY is not configured")

    def search_food(self, food_name):
        url = f"{self.BASE_URL}/foods/search"

        params = {
            "api_key": self.api_key,
            "query": food_name,
            "pageSize": 10
        }

        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        return data.get("foods", [])

    
    
    #the get_food_details method retrieves detailed information about a specific food item using its FDC ID. 
    #It constructs the URL for the USDA API endpoint, makes a GET request with the necessary parameters, 
    #and returns the JSON response containing the food details.
    
    def get_food_details(self, fdc_id):
        url = f"{self.BASE_URL}/food/{fdc_id}"

        response = requests.get(
            url,
            params={"api_key": self.api_key},
            timeout=15
        )

        response.raise_for_status()

        return response.json()



    def get_macros(self, fdc_id):
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

        return macros
