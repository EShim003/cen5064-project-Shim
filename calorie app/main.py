
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
    """Initialize application dependencies and launch login."""

    root = tk.Tk()

    # Shared database for users and food logs
    db_path = "calorie_tracker.db"

    # Authentication dependencies
    user_repository = UserRepository(db_path)
    auth_service = AuthService(user_repository)
    auth_controller = AuthController(auth_service)

    # USDA food search
    usda_service = USDAFoodService()

    # Food log persistence
    food_log_repository = FoodLogRepository(db_path)

    # Existing food log service
    food_log_service = FoodLogService(
        food_log_repository
    )

    # New custom food service
    custom_food_service = CustomFoodService(
        food_log_repository
    )

    def open_food_search(user):
        """Open food tracker after successful login."""

        # Remove login screen widgets
        for widget in root.winfo_children():
            widget.destroy()

        # Initialize food tracker with all dependencies
        CalorieTrackerGUI(
            root=root,
            usda_service=usda_service,
            food_log_service=food_log_service,
            user=user,
            custom_food_service=custom_food_service
        )

    # Start at login screen
    LoginGUI(
        root,
        auth_controller,
        open_food_search
    )

    root.mainloop()


if __name__ == "__main__":
    main()
