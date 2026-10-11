
from service.usda_food_service import USDAFoodService
import requests


def calculate_macros(macros, grams):
    """Calculate nutritional values for a given weight."""

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


def format_nutrient(value, unit):
    """Format nutrition values, including missing data."""

    if value is None:
        return "Not available"

    return f"{value:.2f} {unit}"


def main():
    usda_service = USDAFoodService()

    print("================================")
    print("       CALORIE TRACKER")
    print("================================")

    while True:
        food_name = input(
            "\nEnter a food name (or 'quit'): "
        ).strip()

        if food_name.lower() == "quit":
            print("Goodbye!")
            break

        if not food_name:
            print("Please enter a food name.")
            continue

        try:
            foods = usda_service.search_food(food_name)

            if not foods:
                print("No foods found. Try another search.")
                continue

            print("\nSearch Results:")
            print("--------------------------------")

            for index, food in enumerate(foods, start=1):
                print(
                    f"{index}. {food.get('description')}"
                    f" [{food.get('dataType')}]"
                )

            # Let the user select a food
            while True:
                selection = input(
                    "\nSelect a food number (or 0 to cancel): "
                ).strip()

                try:
                    choice = int(selection)
                except ValueError:
                    print("Please enter a valid number.")
                    continue

                if choice == 0:
                    break

                if not 1 <= choice <= len(foods):
                    print("Invalid selection.")
                    continue

                selected_food = foods[choice - 1]
                fdc_id = selected_food["fdcId"]

                macros = usda_service.get_macros(fdc_id)

                print(f"\nSelected: {macros['name']}")

                # Ask for the quantity in grams
                while True:
                    try:
                        grams = float(
                            input("Enter quantity in grams: ")
                        )

                        if not 0 < grams < float("inf"):
                            print("Enter a positive, finite weight.")
                            continue

                        break

                    except ValueError:
                        print("Please enter a valid number.")

                # Calculate macros for selected weight
                results = calculate_macros(macros, grams)

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
                break

        except requests.RequestException as error:
            print("Unable to contact USDA:", error)


if __name__ == "__main__":
    main()
