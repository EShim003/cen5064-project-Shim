
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class MacroPieChart:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="x", pady=15)

        ttk.Label(
            self.frame,
            text="Daily Macronutrient Breakdown",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.axis = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(
            self.figure,
            master=self.frame
        )

        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

        self.update_chart({
            "protein": 0,
            "carbohydrates": 0,
            "fats": 0
        })

    def update_chart(self, totals):
        self.axis.clear()

        # Get daily macro totals in grams
        protein = max(
            0, float(totals.get("protein") or 0)
        )

        carbs = max(
            0, float(totals.get("carbohydrates") or 0)
        )

        fats = max(
            0, float(totals.get("fats") or 0)
        )

        # Convert grams into calories
        protein_calories = protein * 4
        carb_calories = carbs * 4
        fat_calories = fats * 9

        values = [
            protein_calories,
            carb_calories,
            fat_calories
        ]

        labels = [
            "Protein",
            "Carbohydrates",
            "Fats"
        ]

        colors = [
            "#2563EB",  # Blue - Protein
            "#FACC15",  # Yellow - Carbohydrates
            "#16A34A"   # Green - Fats
        ]

        if sum(values) == 0:
            self.axis.text(
                0.5,
                0.5,
                "No macronutrients logged today",
                ha="center",
                va="center",
                transform=self.axis.transAxes
            )

            self.axis.set_axis_off()

        else:
            self.axis.pie(
                values,
                labels=labels,
                colors=colors,
                autopct="%1.1f%%",
                startangle=90,
                wedgeprops={
                    "edgecolor": "white",
                    "linewidth": 2
                }
            )

            self.axis.axis("equal")

        self.figure.tight_layout()
        self.canvas.draw_idle()

