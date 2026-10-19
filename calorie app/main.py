
from service.usda_food_service import USDAFoodService
from presentation.food_menu import FoodMenu


def main():
    usda_service = USDAFoodService()
    food_menu = FoodMenu(usda_service)

    print("================================")
    print("       CALORIE TRACKER")
    print("================================")

    while True:
        print("\n1. Search USDA Foods")
        print("2. Exit")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            food_menu.search_food()

        elif choice == "2":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
