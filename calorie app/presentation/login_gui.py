
import tkinter as tk
from tkinter import ttk, messagebox


class LoginGUI:

    def __init__(self, root, auth_controller, on_login):
        self.root = root
        self.auth_controller = auth_controller
        self.on_login = on_login

        self.root.title("Calorie Tracker - Login")
        self.root.geometry("450x450")

        self.create_login_widgets()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_login_widgets(self):
        self.clear_window()

        frame = ttk.Frame(self.root, padding=30)
        frame.pack(fill="both", expand=True)

        ttk.Label(
            frame,
            text="Calorie Tracker",
            font=("Arial", 22, "bold")
        ).pack(pady=20)

        ttk.Label(
            frame,
            text="Username"
        ).pack(anchor="w")

        self.username_entry = ttk.Entry(frame)
        self.username_entry.pack(fill="x", pady=5)

        ttk.Label(
            frame,
            text="Password"
        ).pack(anchor="w", pady=(15, 0))

        self.password_entry = ttk.Entry(
            frame,
            show="*"
        )
        self.password_entry.pack(fill="x", pady=5)

        ttk.Button(
            frame,
            text="Log In",
            command=self.login
        ).pack(fill="x", pady=(25, 5))

        ttk.Button(
            frame,
            text="Create Account",
            command=self.create_register_widgets
        ).pack(fill="x", pady=5)

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning(
                "Missing Information",
                "Please enter your username and password."
            )
            return

        try:
            user = self.auth_controller.login(
                username, password
            )

            if not user:
                messagebox.showerror(
                    "Login Failed",
                    "Invalid username or password."
                )
                return

            self.on_login(user)

        except Exception:
            messagebox.showerror(
                "Login Error",
                "Unable to log in. Please try again."
            )

    def create_register_widgets(self):
        self.clear_window()

        frame = ttk.Frame(self.root, padding=30)
        frame.pack(fill="both", expand=True)

        ttk.Label(
            frame,
            text="Create Account",
            font=("Arial", 22, "bold")
        ).pack(pady=20)

        ttk.Label(frame, text="Username").pack(anchor="w")
        self.username_entry = ttk.Entry(frame)
        self.username_entry.pack(fill="x", pady=5)

        ttk.Label(frame, text="Email").pack(anchor="w")
        self.email_entry = ttk.Entry(frame)
        self.email_entry.pack(fill="x", pady=5)

        ttk.Label(frame, text="Password").pack(anchor="w")
        self.password_entry = ttk.Entry(
            frame, show="*"
        )
        self.password_entry.pack(fill="x", pady=5)

        ttk.Button(
            frame,
            text="Register",
            command=self.register
        ).pack(fill="x", pady=(20, 5))

        ttk.Button(
            frame,
            text="Back to Login",
            command=self.create_login_widgets
        ).pack(fill="x", pady=5)

    def register(self):
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get()

        if not username or not email or not password:
            messagebox.showwarning(
                "Missing Information",
                "Please fill in all fields."
            )
            return

        try:
            self.auth_controller.register(
                username, email, password
            )

            messagebox.showinfo(
                "Account Created",
                "Account created successfully. Please log in."
            )

            self.create_login_widgets()

        except ValueError as error:
            messagebox.showerror(
                "Registration Failed",
                str(error)
            )

        except Exception:
            messagebox.showerror(
                "Registration Error",
                "Unable to create account. Please try again."
            )
