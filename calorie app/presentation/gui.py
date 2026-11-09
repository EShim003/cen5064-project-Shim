
import math
import tkinter as tk
from tkinter import ttk, messagebox

from service.macro_calculator import MacroCalculator


class CalorieTrackerGUI:

    def __init__(
        self,
        root,
        usda_service,
        food_log_service=None,
        user=None
    ):
        self.root = root
        self.usda_service = usda_service
        self.food_log_service = food_log_service
        self.user = user

        self.foods = []
        self.log_entries = []

        self.root.title("Calorie & Macro Tracker")
        self.root.geometry("750x800")
        self.root.minsize(600, 500)

        self.create_widgets()
        self.refresh_food_log()

    def create_widgets(self):
        # Main scrollable canvas
        self.canvas = tk.Canvas(
            self.root,
            highlightthickness=0
        )
        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        # Vertical scrollbar
        scrollbar = ttk.Scrollbar(
            self.root,
            orient="vertical",
            command=self.canvas.yview
        )
        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.canvas.configure(
            yscrollcommand=scrollbar.set
        )

        # Frame inside canvas
        frame = ttk.Frame(
            self.canvas,
            padding=20
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=frame,
            anchor="nw"
        )

        # Update scroll region
        def update_scroll_region(event):
            self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )

        frame.bind(
            "<Configure>",
            update_scroll_region
        )

        # Keep frame width equal to canvas width
        def resize_frame(event):
            self.canvas.itemconfigure(
                self.canvas_window,
                width=event.width
            )

        self.canvas.bind(
            "<Configure>",
            resize_frame
        )

        # Mouse wheel scrolling on Windows
        def on_mousewheel(event):
            if event.delta:
                self.canvas.yview_scroll(
                    int(-event.delta / 120),
                    "units"
                )
            return "break"

        # Bind wheel only while mouse is over canvas
        def bind_mousewheel(event):
            self.root.bind_all(
                "<MouseWheel>",
                on_mousewheel
            )

        def unbind_mousewheel(event):
            self.root.unbind_all("<MouseWheel>")

        self.canvas.bind(
            "<Enter>",
            bind_mousewheel
        )
        self.canvas.bind(
            "<Leave>",
            unbind_mousewheel
        )

        # ==============================
        # TITLE
        # ==============================
        ttk.Label(
            frame,
            text="Calorie & Macro Tracker",
            font=("Arial", 20, "bold")
        ).pack(pady=10)

        if self.user:
            ttk.Label(
                frame,
                text=f"Welcome, {self.user['username']}!"
            ).pack(pady=5)

        # ==============================
        # USDA FOOD SEARCH
        # ==============================
        ttk.Label(
            frame,
            text="Search for food:"
        ).pack(anchor="w")

        self.search_entry = ttk.Entry(frame)
        self.search_entry.pack(
            fill="x",
            pady=5
        )

        ttk.Button(
            frame,
            text="Search USDA",
            command=self.search_food
        ).pack(pady=5)

        ttk.Label(
            frame,
            text="Select a food:"
        ).pack(
            anchor="w",
            pady=(10, 5)
        )

        self.food_listbox = tk.Listbox(
            frame,
            height=6
        )
        self.food_listbox.pack(
            fill="x",
            pady=5
        )

        # ==============================
        # FOOD WEIGHT
        # ==============================
        ttk.Label(
            frame,
            text="Quantity in grams:"
        ).pack(
            anchor="w",
            pady=(10, 5)
        )

        self.grams_entry = ttk.Entry(frame)
        self.grams_entry.pack(fill="x")
        self.grams_entry.insert(0, "100")

        ttk.Button(
            frame,
            text="Calculate Nutrition",
            command=self.calculate_nutrition
        ).pack(pady=10)

        # ==============================
        # NUTRITION RESULTS
        # ==============================
        self.result_label = ttk.Label(
            frame,
            text="Search for a food to begin.",
            justify="left"
        )
        self.result_label.pack(
            anchor="w",
            pady=10
        )

        # ==============================
        # ADD TO FOOD LOG
        # ==============================
        ttk.Button(
            frame,
            text="Add to Food Log",
            command=self.add_to_food_log
        ).pack(
            fill="x",
            pady=10
        )

        ttk.Separator(
            frame,
            orient="horizontal"
        ).pack(
            fill="x",
            pady=15
        )

        # ==============================
        # DAILY FOOD LOG
        # ==============================
        ttk.Label(
            frame,
            text="Today's Food Log",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        self.totals_label = ttk.Label(
            frame,
            text=(
                "Calories: 0 kcal\n"
                "Protein: 0 g\n"
                "Carbohydrates: 0 g\n"
                "Fats: 0 g"
            ),
            justify="left"
        )
        self.totals_label.pack(
            anchor="w",
            pady=10
        )

        ttk.Label(
            frame,
            text="Foods Added:"
        ).pack(anchor="w")

        self.log_listbox = tk.Listbox(
            frame,
            height=8
        )
        self.log_listbox.pack(
            fill="x",
            pady=10
        )

        # ==============================
        # REMOVE FOOD BUTTON
        # ==============================
        ttk.Button(
            frame,
            text="Remove Selected Food",
            command=self.remove_selected_food
        ).pack(
            fill="x",
            pady=10
        )

    # ==============================
    # SEARCH USDA FOODS
    # ==============================
    def search_food(self):
        food_name = self.search_entry.get().strip()

        if not food_name:
            messagebox.showwarning(
                "Missing Food",
                "Please enter a food name."
            )
            return

        try:
            foods = self.usda_service.search_food(
                food_name
            )

            self.foods = foods or []

            self.food_listbox.delete(
                0, tk.END
            )

            self.result_label.config(
                text="Select a food and enter its weight."
            )

            if not self.foods:
                messagebox.showinfo(
                    "No Results",
                    "No matching foods were found."
                )
                return

            for food in self.foods:
                self.food_listbox.insert(
                    tk.END,
                    food.get(
                        "description",
                        "Unknown Food"
                    )
                )

        except Exception as error:
            messagebox.showerror(
                "USDA Error",
                str(error)
            )

    # ==============================
    # CALCULATE NUTRITION
    # ==============================
    def calculate_nutrition(self):
        selection = self.food_listbox.curselection()

        if not selection:
            messagebox.showwarning(
                "No Selection",
                "Please select a food."
            )
            return

        try:
            grams = float(
                self.grams_entry.get()
            )

            if not math.isfinite(grams) or grams <= 0:
                raise ValueError(
                    "Weight must be positive and finite."
                )

            selected_food = self.foods[
                selection[0]
            ]

            macros = self.usda_service.get_macros(
                selected_food["fdcId"]
            )

            result = MacroCalculator.calculate(
                macros,
                grams
            )

            def display(value, unit):
                if value is None:
                    return "Not available"

                return f"{value:.2f} {unit}"

            output = (
                f"Food: {macros['name']}\n"
                f"Quantity: {grams:g} g\n"
                f"Calories: {display(result['calories'], 'kcal')}\n"
                f"Protein: {display(result['protein'], 'g')}\n"
                f"Carbs: {display(result['carbohydrates'], 'g')}\n"
                f"Fats: {display(result['fats'], 'g')}"
            )

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

    # ==============================
    # ADD FOOD TO LOG
    # ==============================
    def add_to_food_log(self):
        if (
            self.food_log_service is None
            or self.user is None
        ):
            messagebox.showwarning(
                "Login Required",
                "Please log in before adding food."
            )
            return

        selection = self.food_listbox.curselection()

        if not selection:
            messagebox.showwarning(
                "No Selection",
                "Please select a food first."
            )
            return

        try:
            grams = float(
                self.grams_entry.get()
            )

            if not math.isfinite(grams) or grams <= 0:
                raise ValueError(
                    "Weight must be positive and finite."
                )

            selected_food = self.foods[
                selection[0]
            ]

            macros = self.usda_service.get_macros(
                selected_food["fdcId"]
            )

            self.food_log_service.add_food(
                self.user["id"],
                macros,
                grams
            )

            self.refresh_food_log()

            messagebox.showinfo(
                "Food Added",
                "Food added to your daily log!"
            )

        except ValueError as error:
            messagebox.showerror(
                "Invalid Input",
                str(error)
            )

        except Exception as error:
            messagebox.showerror(
                "Food Log Error",
                str(error)
            )

    # ==============================
    # REFRESH FOOD LOG
    # ==============================
    def refresh_food_log(self):
        if (
            self.food_log_service is None
            or self.user is None
        ):
            return

        try:
            user_id = self.user["id"]

            entries = (
                self.food_log_service.get_daily_log(
                    user_id
                )
            )

            totals = (
                self.food_log_service.get_daily_totals(
                    user_id
                )
            )

            self.log_entries = entries

            self.log_listbox.delete(
                0, tk.END
            )

            for entry in entries:
                self.log_listbox.insert(
                    tk.END,
                    f"{entry['food_name']} - "
                    f"{entry['grams']:g}g - "
                    f"{entry['calories']:.1f} kcal"
                )

            self.totals_label.config(
                text=(
                    f"Calories: {totals['calories']:.1f} kcal\n"
                    f"Protein: {totals['protein']:.1f} g\n"
                    f"Carbohydrates: "
                    f"{totals['carbohydrates']:.1f} g\n"
                    f"Fats: {totals['fats']:.1f} g"
                )
            )

        except Exception as error:
            messagebox.showerror(
                "Food Log Error",
                str(error)
            )

    # ==============================
    # REMOVE FOOD FROM LOG
    # ==============================
    def remove_selected_food(self):
        if (
            self.food_log_service is None
            or self.user is None
        ):
            return

        selection = self.log_listbox.curselection()

        if not selection:
            messagebox.showwarning(
                "No Selection",
                "Select a logged food to remove."
            )
            return

        entry = self.log_entries[
            selection[0]
        ]

        try:
            self.food_log_service.remove_food(
                entry["id"],
                self.user["id"]
            )

            self.refresh_food_log()

        except Exception as error:
            messagebox.showerror(
                "Food Log Error",
                str(error)
            )
