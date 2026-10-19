
import math
import requests

from service.food_service import calculate_macros


def format_nutrient(value, unit):
    """Format nutritional values for display."""

    if value is None:
        return "Not available"

    return f"{value:.2f} {unit}"


class FoodMenu:

    def __init__(self, usda_service):
        self.usda_service = usda_service

    def search_food(self):
        """Search USDA foods and display calculated macros."""

        food_name = input(
            "\nEnter a food name (or 'cancel'): "
        ).strip()

        if food_name.lower() == "cancel":
            return

        if not food_name:
            print("Please enter a food name.")
            return

        try:
            # Search USDA for matching foods
            foods = self.usda_service.search_food(food_name)

            if not foods:
                print("No foods found. Try another search.")
                return

            print("\nUSDA Search Results:")
            print("--------------------------------")

            for index, food in enumerate(foods, start=1):
                print(
                    f"{index}. {food.get('description')}"
                    f" [{food.get('dataType')}]"
                )

            # Ask user to select a food
            while True:
                selection = input(
                    "\nSelect a food number (0 to cancel): "
                ).strip()

                try:
                    choice = int(selection)
                except ValueError:
                    print("Please enter a valid number.")
                    continue

                if choice == 0:
                    return

                if not 1 <= choice <= len(foods):
                    print("Invalid selection.")
                    continue

                selected_food = foods[choice - 1]
                fdc_id = selected_food["fdcId"]

                # Retrieve nutrition information
                macros = self.usda_service.get_macros(fdc_id)

                print(f"\nSelected: {macros['name']}")

                # Ask user for weight in grams
                while True:
                    grams_input = input(
                        "Enter quantity in grams: "
                    ).strip()

                    try:
                        grams = float(grams_input)

                        if not math.isfinite(grams) or grams <= 0:
                            print("Enter a positive, finite weight.")
                            continue

                        break

                    except ValueError:
                        print("Please enter a valid number.")

                # Calculate nutrition for the entered weight
                results = calculate_macros(macros, grams)

                # Display results
                print("\n================================")
                print("         NUTRITION FACTS")
                print("================================")
                print(f"Food: {macros['name']}")
                print(f"Quantity: {grams:g} g")
                print("--------------------------------")

                print(
                    "Calories:",
                    format_nutrient(results["calories"], "kcal")
                )
                print(
                    "Protein:",
                    format_nutrient(results["protein"], "g")
                )
                print(
                    "Carbohydrates:",
                    format_nutrient(
                        results["carbohydrates"], "g"
                    )
                )
                print(
                    "Fats:",
                    format_nutrient(results["fats"], "g")
                )

                print("================================")
                return

        except requests.RequestException as error:
            print("Unable to contact USDA:", error)
