
import unittest
from unittest.mock import Mock, patch

from presentation.gui import CalorieTrackerGUI


class TestCalorieTrackerGUI(unittest.TestCase):

    def setUp(self):
        # Create GUI instance without opening a Tkinter window
        self.gui = CalorieTrackerGUI.__new__(
            CalorieTrackerGUI
        )

        # Mock dependencies
        self.gui.usda_service = Mock()
        self.gui.food_log_service = Mock()
        self.gui.custom_food_service = Mock()

        # Initialize food data
        self.gui.foods = []
        self.gui.log_entries = []

        # Mock GUI widgets
        self.gui.search_entry = Mock()
        self.gui.food_listbox = Mock()
        self.gui.grams_entry = Mock()
        self.gui.result_label = Mock()
        self.gui.log_tree = Mock()
        self.gui.totals_label = Mock()
        self.gui.macro_chart = Mock()

        # Mock logged-in user
        self.gui.user = {
            "id": 1,
            "username": "testuser"
        }

        # Initialize custom food windows
        self.gui.custom_food_windows = []

        # Mock logout callback
        self.gui.on_logout = Mock()

        # Mock mousewheel cleanup
        self.gui.disable_mousewheel = Mock()

    @patch("presentation.gui.messagebox.showwarning")
    def test_search_empty_food(self, mock_warning):
        # Empty searches should display a warning
        self.gui.search_entry.get.return_value = " "

        self.gui.search_food()

        mock_warning.assert_called_once_with(
            "Missing Food",
            "Please enter a food name."
        )

        self.gui.usda_service.search_food.assert_not_called()

    def test_search_food_successfully(self):
        # USDA search should populate the listbox
        self.gui.search_entry.get.return_value = "Banana"

        self.gui.usda_service.search_food.return_value = [
            {
                "fdcId": 123,
                "description": "Bananas, raw"
            }
        ]

        self.gui.search_food()

        self.gui.usda_service.search_food.assert_called_once_with(
            "Banana"
        )

        self.assertEqual(len(self.gui.foods), 1)

        self.gui.food_listbox.insert.assert_called_once_with(
            "end",
            "Bananas, raw"
        )

    @patch("presentation.gui.messagebox.showinfo")
    def test_search_no_results(self, mock_info):
        # No matching foods should display a message
        self.gui.search_entry.get.return_value = "Unknown"

        self.gui.usda_service.search_food.return_value = []

        self.gui.search_food()

        mock_info.assert_called_once_with(
            "No Results",
            "No matching foods were found."
        )

        self.assertEqual(self.gui.foods, [])

    @patch("presentation.gui.messagebox.showerror")
    def test_calculate_without_selection(self, mock_error):
        # Calculation requires a selected food
        self.gui.food_listbox.curselection.return_value = ()

        self.gui.calculate_nutrition()

        mock_error.assert_called_once_with(
            "Invalid Input",
            "Please select a food first."
        )

        self.gui.usda_service.get_macros.assert_not_called()

    @patch("presentation.gui.messagebox.showerror")
    def test_calculate_invalid_weight(self, mock_error):
        # Negative weights should be rejected
        self.gui.foods = [
            {
                "fdcId": 123,
                "description": "Bananas, raw"
            }
        ]

        self.gui.food_listbox.curselection.return_value = (0,)
        self.gui.grams_entry.get.return_value = "-50"

        self.gui.calculate_nutrition()

        mock_error.assert_called_once_with(
            "Invalid Input",
            "Weight must be positive and finite."
        )

        self.gui.usda_service.get_macros.assert_not_called()

    @patch("presentation.gui.messagebox.showerror")
    def test_calculate_nutrition_successfully(self, mock_error):
        # Calculate nutrition for 150 grams of banana
        self.gui.foods = [
            {
                "fdcId": 123,
                "description": "Bananas, raw"
            }
        ]

        self.gui.food_listbox.curselection.return_value = (0,)
        self.gui.grams_entry.get.return_value = "150"

        self.gui.usda_service.get_macros.return_value = {
            "name": "Bananas, raw",
            "calories": 89,
            "protein": 1.09,
            "carbohydrates": 22.84,
            "fats": 0.33
        }

        self.gui.calculate_nutrition()

        self.gui.usda_service.get_macros.assert_called_once_with(
            123
        )

        # Verify displayed nutritional values
        output = (
            self.gui.result_label.config.call_args.kwargs[
                "text"
            ]
        )

        self.assertIn("Bananas, raw", output)
        self.assertIn("150 g", output)
        self.assertIn("133.50 kcal", output)
        self.assertIn("1.64 g", output)
        self.assertIn("34.26 g", output)
        self.assertIn("0.49 g", output)

        mock_error.assert_not_called()

    @patch("presentation.gui.messagebox.showerror")
    def test_calculate_missing_nutrient(self, mock_error):
        # Missing USDA nutrients should display Not available
        self.gui.foods = [
            {
                "fdcId": 123,
                "description": "Test Food"
            }
        ]

        self.gui.food_listbox.curselection.return_value = (0,)
        self.gui.grams_entry.get.return_value = "100"

        self.gui.usda_service.get_macros.return_value = {
            "name": "Test Food",
            "calories": 100,
            "protein": None,
            "carbohydrates": 20,
            "fats": 5
        }

        self.gui.calculate_nutrition()

        output = (
            self.gui.result_label.config.call_args.kwargs[
                "text"
            ]
        )

        self.assertIn(
            "Protein: Not available",
            output
        )

        mock_error.assert_not_called()

    def test_logout(self):
        # Set up a logged-in user
        self.gui.user = {
            "id": 1,
            "username": "testuser"
        }

        # Add temporary food search data
        self.gui.foods = [
            {
                "fdcId": 123,
                "description": "Bananas, raw"
            }
        ]

        # Add temporary food log data
        self.gui.log_entries = [
            {
                "id": 1,
                "food_name": "Bananas, raw"
            }
        ]

        # Log out the user
        self.gui.logout()

        # Verify the current user is cleared
        self.assertIsNone(self.gui.user)

        # Verify temporary data is cleared
        self.assertEqual(self.gui.foods, [])
        self.assertEqual(self.gui.log_entries, [])

        # Verify custom food windows are cleared
        self.assertEqual(self.gui.custom_food_windows, [])

        # Verify mousewheel bindings are removed
        self.gui.disable_mousewheel.assert_called_once()

        # Verify login callback is triggered
        self.gui.on_logout.assert_called_once()


if __name__ == "__main__":
    unittest.main()
