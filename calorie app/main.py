
import tkinter as tk

from presentation.gui import CalorieTrackerGUI
from presentation.login_gui import LoginGUI

from controller.auth_controller import AuthController
from service.auth_service import AuthService
from repository.user_repository import UserRepository

from service.usda_food_service import USDAFoodService
from service.food_log_service import FoodLogService
from repository.food_log_repository import FoodLogRepository


def main():
    root = tk.Tk()

    # Authentication
    user_repository = UserRepository("calorie_tracker.db")
    auth_service = AuthService(user_repository)
    auth_controller = AuthController(auth_service)

    # USDA food search
    usda_service = USDAFoodService()

    # Food log storage
    food_log_repository = FoodLogRepository(
        "calorie_tracker.db"
    )
    food_log_service = FoodLogService(
        food_log_repository
    )

    def open_food_search(user):
        # Remove login screen
        for widget in root.winfo_children():
            widget.destroy()

        # Open food search with logged-in user
        CalorieTrackerGUI(
            root,
            usda_service,
            food_log_service,
            user
        )

    # Login first
    LoginGUI(
        root,
        auth_controller,
        open_food_search
    )

    root.mainloop()


if __name__ == "__main__":
    main()
