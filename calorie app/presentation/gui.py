
import math
import tkinter as tk
from tkinter import ttk, messagebox

from service.macro_calculator import MacroCalculator


class CalorieTrackerGUI:

    def __init__(self, root, usda_service):
        self.root = root
        self.usda_service = usda_service
        self.foods = []

        self.root.title("Calorie & Macro Tracker")
        self.root.geometry("650x600")
        self.root.minsize(550, 500)

        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)

        # Application title
        title = ttk.Label(
            frame,
            text="Calorie & Macro Tracker",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=10)

        # Food search input
        ttk.Label(
            frame,
            text="Search for food:"
        ).pack(anchor="w")

        self.search_entry = ttk.Entry(frame)
        self.search_entry.pack(fill="x", pady=5)

        ttk.Button(
            frame,
            text="Search USDA",
            command=self.search_food
        ).pack(pady=8)

        # USDA search results
        ttk.Label(
            frame,
            text="Select a food:"
        ).pack(anchor="w", pady=(10, 5))

        self.food_listbox = tk.Listbox(
            frame,
            height=9
        )
        self.food_listbox.pack(
            fill="both",
            expand=True
        )

        # Food weight input
        ttk.Label(
            frame,
            text="Quantity in grams:"
        ).pack(anchor="w", pady=(12, 5))

        self.grams_entry = ttk.Entry(frame)
        self.grams_entry.pack(fill="x")
        self.grams_entry.insert(0, "100")

        # Calculate button
        ttk.Button(
            frame,
            text="Calculate Nutrition",
            command=self.calculate_nutrition
        ).pack(pady=15)

        # Nutrition results
        self.result_label = ttk.Label(
            frame,
            text="Search for a food to begin.",
            font=("Arial", 11),
            justify="left"
        )
        self.result_label.pack(
            anchor="w",
            pady=10
        )

    def search_food(self):
        food_name = self.search_entry.get().strip()

        # Validate search input
        if not food_name:
            messagebox.showwarning(
                "Missing Food",
                "Please enter a food name."
            )
            return

        try:
            # Search USDA FoodData Central
            self.foods = self.usda_service.search_food(
                food_name
            )

            # Clear previous results
            self.food_listbox.delete(0, tk.END)

            self.result_label.config(
                text="Select a food and enter its weight."
            )

            if not self.foods:
                messagebox.showinfo(
                    "No Results",
                    "No matching foods were found."
                )
                return

            # Display USDA food descriptions
            for food in self.foods:
                self.food_listbox.insert(
                    tk.END,
                    food.get("description", "Unknown Food")
                )

        except Exception as error:
            messagebox.showerror(
                "USDA Error",
                str(error)
            )

    def calculate_nutrition(self):
        selection = self.food_listbox.curselection()

        # Require a selected food
        if not selection:
            messagebox.showwarning(
                "No Selection",
                "Please select a food."
            )
            return

        try:
            # Get and validate weight
            grams = float(self.grams_entry.get())

            if not math.isfinite(grams) or grams <= 0:
                raise ValueError(
                    "Weight must be positive and finite."
                )

            # Retrieve selected USDA food
            selected_food = self.foods[selection[0]]

            # Get nutrition information per 100g
            macros = self.usda_service.get_macros(
                selected_food["fdcId"]
            )

            # Calculate nutrition using MacroCalculator
            result = MacroCalculator.calculate(
                macros,
                grams
            )

            # Format nutrient values
            def display(value, unit):
                if value is None:
                    return "Not available"

                return f"{value:.2f} {unit}"

            # Build nutrition output
            output = (
                f"Food: {macros['name']}\n"
                f"Quantity: {grams:g} g\n\n"
                f"Calories: "
                f"{display(result['calories'], 'kcal')}\n"
                f"Protein: "
                f"{display(result['protein'], 'g')}\n"
                f"Carbohydrates: "
                f"{display(result['carbohydrates'], 'g')}\n"
                f"Fats: "
                f"{display(result['fats'], 'g')}"
            )

            # Display calculated nutrition
            self.result_label.config(
                text=output
            )

        except ValueError as error:
            messagebox.showerror(
                "Invalid Input",
                str(error)
            )

        except Exception as error:
            messagebox.showerror(
                "Calculation Error",
                str(error)
            )
