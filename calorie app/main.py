
import tkinter as tk

from presentation.gui import CalorieTrackerGUI
from presentation.login_gui import LoginGUI

from controller.auth_controller import AuthController
from service.auth_service import AuthService
from repository.user_repository import UserRepository
from service.usda_food_service import USDAFoodService


def main():
    root = tk.Tk()

    # Initialize authentication
    user_repository = UserRepository("calorie_tracker.db")
    auth_service = AuthService(user_repository)
    auth_controller = AuthController(auth_service)

    # Initialize USDA service
    usda_service = USDAFoodService()

    def open_food_search(user):
        # Clear login screen
        for widget in root.winfo_children():
            widget.destroy()

        # Launch food search GUI
        CalorieTrackerGUI(root, usda_service)

    # Display login screen first
    LoginGUI(root, auth_controller, open_food_search)

    root.mainloop()


if __name__ == "__main__":
    main()
