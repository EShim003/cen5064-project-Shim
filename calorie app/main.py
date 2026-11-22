
import tkinter as tk

from presentation.gui import CalorieTrackerGUI
from presentation.login_gui import LoginGUI

from controller.auth_controller import AuthController

from service.auth_service import AuthService
from service.usda_food_service import USDAFoodService
from service.food_log_service import FoodLogService
from service.custom_food_service import CustomFoodService

from repository.user_repository import UserRepository
from repository.food_log_repository import FoodLogRepository


def main():
    root = tk.Tk()

    db_path = "calorie_tracker.db"

    # Initialize repositories
    user_repository = UserRepository(db_path)
    food_log_repository = FoodLogRepository(db_path)

    # Initialize services
    auth_service = AuthService(user_repository)
    auth_controller = AuthController(auth_service)

    usda_service = USDAFoodService()
    food_log_service = FoodLogService(food_log_repository)
    custom_food_service = CustomFoodService(food_log_repository)

    def clear_window():
        # Remove all widgets from the current screen
        for widget in root.winfo_children():
            widget.destroy()

    def show_login():
        # Return to the login screen
        clear_window()

        LoginGUI(
            root,
            auth_controller,
            open_food_search
        )

    def open_food_search(user):
        # Open the calorie tracker after login
        clear_window()

        CalorieTrackerGUI(
            root=root,
            usda_service=usda_service,
            food_log_service=food_log_service,
            user=user,
            custom_food_service=custom_food_service,
            on_logout=show_login
        )

    # Start application at login screen
    show_login()

    root.mainloop()


if __name__ == "__main__":
    main()

