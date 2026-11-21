
import unittest
from unittest.mock import Mock

from presentation.macro_chart import MacroPieChart


class TestMacroPieChart(unittest.TestCase):

    def setUp(self):
        # Create chart without opening Tkinter
        self.chart = MacroPieChart.__new__(
            MacroPieChart
        )

        self.chart.axis = Mock()
        self.chart.figure = Mock()
        self.chart.canvas = Mock()

    def test_chart_displays_macronutrients(self):
        totals = {
            "protein": 120,
            "carbohydrates": 150,
            "fats": 60
        }

        self.chart.update_chart(totals)

        self.chart.axis.pie.assert_called_once()

        args, kwargs = self.chart.axis.pie.call_args

        self.assertEqual(
            args[0],
            [120.0, 150.0, 60.0]
        )

        self.assertEqual(
            kwargs["labels"],
            [
                "Protein",
                "Carbohydrates",
                "Fats"
            ]
        )

        self.assertEqual(
            kwargs["colors"],
            [
                "#2563EB",
                "#FACC15",
                "#16A34A"
            ]
        )

        self.chart.canvas.draw_idle.assert_called_once()

    def test_chart_handles_empty_food_log(self):
        totals = {
            "protein": 0,
            "carbohydrates": 0,
            "fats": 0
        }

        self.chart.update_chart(totals)

        self.chart.axis.pie.assert_not_called()
        self.chart.axis.text.assert_called_once()
        self.chart.axis.set_axis_off.assert_called_once()

    def test_chart_handles_missing_nutrients(self):
        totals = {
            "protein": None,
            "carbohydrates": 50,
            "fats": None
        }

        self.chart.update_chart(totals)

        args, kwargs = self.chart.axis.pie.call_args

        self.assertEqual(
            args[0],
            [0.0, 50.0, 0.0]
        )


if __name__ == "__main__":
    unittest.main()
