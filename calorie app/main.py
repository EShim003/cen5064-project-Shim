
from service.usda_food_service import USDAFoodService

def main():
    usda_service = USDAFoodService()

    food_name = input("Search for a food: ")

    try:
        results = usda_service.search_food(food_name)

        if not results:
            print("No foods found.")
            return

        for food in results:
            print("----------------------")
            print("Name:", food.get("description"))
            print("FDC ID:", food.get("fdcId"))
            print("Type:", food.get("dataType"))

    except Exception as error:
        print("Error retrieving food:", error)


if __name__ == "__main__":
    main()
