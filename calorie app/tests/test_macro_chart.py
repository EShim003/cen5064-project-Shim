
import unittest
from unittest.mock import Mock

from presentation.macro_chart import MacroPieChart


class TestMacroPieChart(unittest.TestCase):

    def setUp(self):
        # Avoid creating a real Tkinter window
        self.chart = MacroPieChart.__new__(MacroPieChart)

        self.chart.axis = Mock()
        self.chart.figure = Mock()
        self.chart.canvas = Mock()

    def test_macro_percentages(self):
        totals = {
            "protein": 150,
            "carbohydrates": 150,
            "fats": 33.33
        }

        self.chart.update_chart(totals)

        # Protein: 150 * 4 = 600 calories
        # Carbs: 150 * 4 = 600 calories
        # Fats: 33.33 * 9 = 299.97 calories

        args, kwargs = self.chart.axis.pie.call_args

        self.assertEqual(
            args[0],
            [600, 600, 299.97]
        )

        self.assertEqual(
            kwargs["autopct"],
            "%1.1f%%"
        )

        self.assertEqual(
            kwargs["colors"],
            ["#2563EB", "#FACC15", "#16A34A"]
        )

    def test_empty_macro_chart(self):
        totals = {
            "protein": 0,
            "carbohydrates": 0,
            "fats": 0
        }

        self.chart.update_chart(totals)

        self.chart.axis.pie.assert_not_called()
        self.chart.axis.text.assert_called_once()
        self.chart.axis.set_axis_off.assert_called_once()

    def test_missing_macros(self):
        totals = {
            "protein": 25
        }

        self.chart.update_chart(totals)

        args, kwargs = self.chart.axis.pie.call_args

        self.assertEqual(
            args[0],
            [100, 0, 0]
        )

        self.assertEqual(
            kwargs["autopct"],
            "%1.1f%%"
        )


if __name__ == "__main__":
    unittest.main()

