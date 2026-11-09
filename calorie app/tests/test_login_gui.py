
import unittest
from unittest.mock import Mock, patch

from presentation.login_gui import LoginGUI


class TestLoginGUI(unittest.TestCase):

    def setUp(self):
        # Create GUI object without opening Tkinter
        self.gui = LoginGUI.__new__(LoginGUI)

        # Mock authentication controller and callback
        self.gui.auth_controller = Mock()
        self.gui.on_login = Mock()

        # Mock entry widgets
        self.gui.username_entry = Mock()
        self.gui.password_entry = Mock()
        self.gui.email_entry = Mock()

    @patch("presentation.login_gui.messagebox.showwarning")
    def test_login_empty_fields(self, mock_warning):
        # Empty username and password
        self.gui.username_entry.get.return_value = ""
        self.gui.password_entry.get.return_value = ""

        self.gui.login()

        mock_warning.assert_called_once_with(
            "Missing Information",
            "Please enter your username and password."
        )

        self.gui.auth_controller.login.assert_not_called()

    @patch("presentation.login_gui.messagebox.showerror")
    def test_login_invalid_credentials(self, mock_error):
        # Invalid username or password
        self.gui.username_entry.get.return_value = "testuser"
        self.gui.password_entry.get.return_value = "wrongpassword"

        self.gui.auth_controller.login.return_value = None

        self.gui.login()

        mock_error.assert_called_once_with(
            "Login Failed",
            "Invalid username or password."
        )

        self.gui.on_login.assert_not_called()

    @patch("presentation.login_gui.messagebox.showerror")
    def test_login_successfully(self, mock_error):
        # Valid login credentials
        self.gui.username_entry.get.return_value = "testuser"
        self.gui.password_entry.get.return_value = "password123"

        user = {
            "id": 1,
            "username": "testuser",
            "email": "test@example.com"
        }

        self.gui.auth_controller.login.return_value = user

        self.gui.login()

        self.gui.auth_controller.login.assert_called_once_with(
            "testuser",
            "password123"
        )

        self.gui.on_login.assert_called_once_with(user)
        mock_error.assert_not_called()

    @patch("presentation.login_gui.messagebox.showwarning")
    def test_register_empty_fields(self, mock_warning):
        # Missing registration information
        self.gui.username_entry.get.return_value = "testuser"
        self.gui.email_entry.get.return_value = ""
        self.gui.password_entry.get.return_value = "password123"

        self.gui.register()

        mock_warning.assert_called_once_with(
            "Missing Information",
            "Please fill in all fields."
        )

        self.gui.auth_controller.register.assert_not_called()

    @patch("presentation.login_gui.messagebox.showinfo")
    def test_register_successfully(self, mock_info):
        # Successful registration
        self.gui.username_entry.get.return_value = "testuser"
        self.gui.email_entry.get.return_value = "test@example.com"
        self.gui.password_entry.get.return_value = "password123"

        self.gui.auth_controller.register.return_value = 1

        # Mock screen transition
        self.gui.create_login_widgets = Mock()

        self.gui.register()

        self.gui.auth_controller.register.assert_called_once_with(
            "testuser",
            "test@example.com",
            "password123"
        )

        mock_info.assert_called_once_with(
            "Account Created",
            "Account created successfully. Please log in."
        )

        self.gui.create_login_widgets.assert_called_once()

    @patch("presentation.login_gui.messagebox.showerror")
    def test_register_duplicate_username(self, mock_error):
        # Duplicate username should show an error
        self.gui.username_entry.get.return_value = "testuser"
        self.gui.email_entry.get.return_value = "test@example.com"
        self.gui.password_entry.get.return_value = "password123"

        self.gui.auth_controller.register.side_effect = ValueError(
            "Username already exists."
        )

        self.gui.register()

        mock_error.assert_called_once_with(
            "Registration Failed",
            "Username already exists."
        )

    @patch("presentation.login_gui.messagebox.showerror")
    def test_register_short_password(self, mock_error):
        # Password validation from AuthService
        self.gui.username_entry.get.return_value = "testuser"
        self.gui.email_entry.get.return_value = "test@example.com"
        self.gui.password_entry.get.return_value = "123"

        self.gui.auth_controller.register.side_effect = ValueError(
            "Password must be at least 8 characters."
        )

        self.gui.register()

        mock_error.assert_called_once_with(
            "Registration Failed",
            "Password must be at least 8 characters."
        )


if __name__ == "__main__":
    unittest.main()
