
import math
import tkinter as tk
from tkinter import ttk, messagebox

from service.macro_calculator import MacroCalculator


class CalorieTrackerGUI:
    """GUI for searching, calculating, and logging foods."""

    def __init__(
        self,
        root,
        usda_service,
        food_log_service=None,
        user=None,
        custom_food_service=None
    ):
        self.root = root
        self.usda_service = usda_service
        self.food_log_service = food_log_service
        self.custom_food_service = custom_food_service
        self.user = user

        self.foods = []
        self.log_entries = []

        self.root.title("Calorie & Macro Tracker")
        self.root.geometry("850x800")
        self.root.minsize(600, 500)

        self.create_widgets()
        self.refresh_food_log()

    def create_widgets(self):
        """Create the scrollable application interface."""

        # MAIN SCROLLABLE CANVAS
        self.canvas = tk.Canvas(
            self.root,
            highlightthickness=0
        )
        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar = ttk.Scrollbar(
            self.root,
            orient="vertical",
            command=self.canvas.yview
        )
        scrollbar.pack(side="right", fill="y")

        self.canvas.configure(
            yscrollcommand=scrollbar.set
        )

        frame = ttk.Frame(self.canvas, padding=20)

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=frame,
            anchor="nw"
        )

        frame.bind(
            "<Configure>",
            lambda event: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.bind(
            "<Configure>",
            lambda event: self.canvas.itemconfigure(
                self.canvas_window,
                width=event.width
            )
        )

        # Mouse-wheel scrolling
        self.canvas.bind(
            "<Enter>",
            self.enable_mousewheel
        )
        self.canvas.bind(
            "<Leave>",
            self.disable_mousewheel
        )

        frame.bind(
            "<Enter>",
            self.enable_mousewheel
        )

        # TITLE
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

        # USDA FOOD SEARCH
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
        ).pack(pady=5)

        ttk.Label(
            frame,
            text="Select a food:"
        ).pack(anchor="w", pady=(10, 5))

        self.food_listbox = tk.Listbox(
            frame,
            height=6,
            exportselection=False
        )
        self.food_listbox.pack(fill="x", pady=5)

        # FOOD WEIGHT
        ttk.Label(
            frame,
            text="Quantity in grams:"
        ).pack(anchor="w", pady=(10, 5))

        self.grams_entry = ttk.Entry(frame)
        self.grams_entry.pack(fill="x")
        self.grams_entry.insert(0, "100")

        ttk.Button(
            frame,
            text="Calculate Nutrition",
            command=self.calculate_nutrition
        ).pack(pady=10)

        # NUTRITION RESULTS
        self.result_label = ttk.Label(
            frame,
            text="Search for a food to begin.",
            justify="left"
        )
        self.result_label.pack(anchor="w", pady=10)

        # ADD SEARCHED FOOD
        ttk.Button(
            frame,
            text="Add to Food Log",
            command=self.add_to_food_log
        ).pack(fill="x", pady=5)

        # ADD CUSTOM FOOD
        ttk.Button(
            frame,
            text="Add Custom Food",
            command=self.open_custom_food_window
        ).pack(fill="x", pady=5)

        ttk.Separator(
            frame,
            orient="horizontal"
        ).pack(fill="x", pady=15)

        # DAILY FOOD LOG
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
        self.totals_label.pack(anchor="w", pady=10)

        ttk.Label(
            frame,
            text="Foods Added:"
        ).pack(anchor="w")

        # FOOD LOG TABLE
        table_frame = ttk.Frame(frame)
        table_frame.pack(
            fill="x",
            pady=10
        )

        columns = (
            "food",
            "grams",
            "calories",
            "protein",
            "carbohydrates",
            "fats"
        )

        self.log_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=8,
            selectmode="browse"
        )

        headings = {
            "food": "Food Name",
            "grams": "Weight (g)",
            "calories": "Calories (kcal)",
            "protein": "Protein (g)",
            "carbohydrates": "Carbs (g)",
            "fats": "Fats (g)"
        }

        for column, heading in headings.items():
            self.log_tree.heading(
                column,
                text=heading
            )

        self.log_tree.column(
            "food",
            width=220,
            minwidth=150,
            anchor="w"
        )

        for column in columns[1:]:
            self.log_tree.column(
                column,
                width=110,
                minwidth=85,
                anchor="center"
            )

        table_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.log_tree.yview
        )

        horizontal_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.log_tree.xview
        )

        self.log_tree.configure(
            yscrollcommand=table_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set
        )

        self.log_tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        table_scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        horizontal_scrollbar.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        # REMOVE FOOD BUTTON
        ttk.Button(
            frame,
            text="Remove Selected Food",
            command=self.remove_selected_food
        ).pack(fill="x", pady=10)

    # ==============================
    # MOUSE-WHEEL SCROLLING
    # ==============================
    def enable_mousewheel(self, event=None):
        self.root.bind_all(
            "<MouseWheel>",
            self.on_mousewheel
        )

    def disable_mousewheel(self, event=None):
        self.root.unbind_all("<MouseWheel>")

    def on_mousewheel(self, event):
        if event.delta:
            self.canvas.yview_scroll(
                int(-event.delta / 120),
                "units"
            )
        return "break"

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
            self.foods = (
                self.usda_service.search_food(food_name) or []
            )

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

    # ==============================
    # VALIDATE USDA SELECTION
    # ==============================
    def get_selected_food_and_grams(self):
        selection = self.food_listbox.curselection()

        if not selection:
            raise ValueError(
                "Please select a food first."
            )

        try:
            grams = float(
                self.grams_entry.get()
            )
        except ValueError:
            raise ValueError(
                "Please enter a valid weight."
            ) from None

        if not math.isfinite(grams) or grams <= 0:
            raise ValueError(
                "Weight must be positive and finite."
            )

        selected_food = self.foods[selection[0]]

        return selected_food, grams

    # ==============================
    # CALCULATE NUTRITION
    # ==============================
    def calculate_nutrition(self):
        try:
            selected_food, grams = (
                self.get_selected_food_and_grams()
            )

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
                f"Calories: "
                f"{display(result['calories'], 'kcal')}\n"
                f"Protein: "
                f"{display(result['protein'], 'g')}\n"
                f"Carbs: "
                f"{display(result['carbohydrates'], 'g')}\n"
                f"Fats: "
                f"{display(result['fats'], 'g')}"
            )

            self.result_label.config(text=output)

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
    # ADD SEARCHED FOOD TO LOG
    # ==============================
    def add_to_food_log(self):
        if self.user is None or self.food_log_service is None:
            messagebox.showwarning(
                "Login Required",
                "Please log in before adding food."
            )
            return

        try:
            selected_food, grams = (
                self.get_selected_food_and_grams()
            )

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
    # OPEN CUSTOM FOOD WINDOW
    # ==============================
    def open_custom_food_window(self):
        if self.user is None or self.custom_food_service is None:
            messagebox.showwarning(
                "Login Required",
                "Please log in before adding food."
            )
            return

        window = tk.Toplevel(self.root)
        window.title("Add Custom Food")
        window.geometry("450x550")
        window.minsize(400, 500)

        frame = ttk.Frame(window, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(
            frame,
            text="Add Custom Food",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        ttk.Label(
            frame,
            text="Enter nutrition for the amount consumed."
        ).pack(pady=5)

        fields = [
            ("Food Name", "name"),
            ("Amount in Grams", "grams"),
            ("Calories (kcal)", "calories"),
            ("Protein (g)", "protein"),
            ("Carbohydrates (g)", "carbohydrates"),
            ("Fats (g)", "fats")
        ]

        entries = {}

        for label_text, key in fields:
            ttk.Label(
                frame,
                text=label_text
            ).pack(anchor="w", pady=(8, 0))

            entry = ttk.Entry(frame)
            entry.pack(fill="x", pady=2)
            entries[key] = entry

        entries["grams"].insert(0, "100")

        ttk.Button(
            frame,
            text="Save to Food Log",
            command=lambda: self.save_custom_food(
                entries,
                window
            )
        ).pack(fill="x", pady=20)

        entries["name"].focus_set()

    # ==============================
    # SAVE CUSTOM FOOD
    # ==============================
    def save_custom_food(self, entries, window):
        if self.user is None or self.custom_food_service is None:
            messagebox.showwarning(
                "Login Required",
                "Please log in before adding food."
            )
            return

        try:
            name = entries["name"].get().strip()

            numeric_fields = [
                "grams",
                "calories",
                "protein",
                "carbohydrates",
                "fats"
            ]

            values = {}

            for field in numeric_fields:
                text = entries[field].get().strip()

                if not text:
                    raise ValueError(
                        f"{field.capitalize()} is required."
                    )

                values[field] = float(text)

            self.custom_food_service.add_custom_food(
                user_id=self.user["id"],
                name=name,
                grams=values["grams"],
                calories=values["calories"],
                protein=values["protein"],
                carbohydrates=values["carbohydrates"],
                fats=values["fats"]
            )

            self.refresh_food_log()

            window.destroy()

            messagebox.showinfo(
                "Food Added",
                "Custom food added to your daily log!"
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
    # REFRESH FOOD LOG TABLE
    # ==============================
    def refresh_food_log(self):
        if self.user is None or self.food_log_service is None:
            return

        try:
            user_id = self.user["id"]

            entries = self.food_log_service.get_daily_log(
                user_id
            )

            totals = self.food_log_service.get_daily_totals(
                user_id
            )

            self.log_entries = entries

            # Clear existing rows
            for item in self.log_tree.get_children():
                self.log_tree.delete(item)

            # Add each food with labeled macros
            for index, entry in enumerate(entries):
                self.log_tree.insert(
                    "",
                    "end",
                    iid=str(index),
                    values=(
                        entry["food_name"],
                        f"{entry['grams']:.1f}",
                        f"{entry['calories']:.1f}",
                        f"{entry['protein']:.1f}",
                        f"{entry['carbohydrates']:.1f}",
                        f"{entry['fats']:.1f}"
                    )
                )

            # Update daily totals
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
    # REMOVE SELECTED FOOD
    # ==============================
    def remove_selected_food(self):
        if self.user is None or self.food_log_service is None:
            return

        selection = self.log_tree.selection()

        if not selection:
            messagebox.showwarning(
                "No Selection",
                "Select a logged food to remove."
            )
            return

        index = int(selection[0])
        entry = self.log_entries[index]

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
