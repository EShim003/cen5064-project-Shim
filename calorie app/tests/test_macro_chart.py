
import unittest
from unittest.mock import Mock

from presentation.macro_chart import MacroPieChart


class TestMacroPieChart(unittest.TestCase):

    def setUp(self):
        # Create the chart without opening a Tkinter window
        # This allows tests to run in GitHub Actions
        self.chart = MacroPieChart.__new__(MacroPieChart)

        # Mock Matplotlib components
        self.chart.axis = Mock()
        self.chart.figure = Mock()
        self.chart.canvas = Mock()

    def test_macro_percentages(self):
        # Example daily macronutrient totals
        totals = {
            "protein": 150,
            "carbohydrates": 150,
            "fats": 33.33
        }

        # Update the pie chart
        self.chart.update_chart(totals)

        # Expected calorie calculations:
        # Protein: 150 * 4 = 600 calories
        # Carbohydrates: 150 * 4 = 600 calories
        # Fats: 33.33 * 9 = 299.97 calories

        args, kwargs = self.chart.axis.pie.call_args

        expected_values = [600, 600, 299.97]
        actual_values = args[0]

        # Verify all three macronutrients are included
        self.assertEqual(len(actual_values), 3)

        # Allow small floating-point precision differences
        for actual, expected in zip(
            actual_values,
            expected_values
        ):
            self.assertAlmostEqual(
                actual,
                expected,
                places=2
            )

        # Verify the chart displays percentages
        self.assertEqual(
            kwargs["autopct"],
            "%1.1f%%"
        )

        # Verify macronutrient labels
        self.assertEqual(
            kwargs["labels"],
            [
                "Protein",
                "Carbohydrates",
                "Fats"
            ]
        )

        # Verify chart colors
        self.assertEqual(
            kwargs["colors"],
            [
                "#2563EB",  # Blue - Protein
                "#FACC15",  # Yellow - Carbohydrates
                "#16A34A"   # Green - Fats
            ]
        )

        # Verify the chart is redrawn
        self.chart.canvas.draw_idle.assert_called_once()

    def test_empty_macro_chart(self):
        # No food has been logged
        totals = {
            "protein": 0,
            "carbohydrates": 0,
            "fats": 0
        }

        self.chart.update_chart(totals)

        # Pie chart should not be created for zero macros
        self.chart.axis.pie.assert_not_called()

        # Verify empty chart message is displayed
        self.chart.axis.text.assert_called_once()

        text_args, text_kwargs = (
            self.chart.axis.text.call_args
        )

        self.assertIn(
            "No macronutrients logged today",
            text_args
        )

        # Verify chart axes are hidden
        self.chart.axis.set_axis_off.assert_called_once()

        # Verify chart is redrawn
        self.chart.canvas.draw_idle.assert_called_once()

    def test_missing_macros(self):
        # Only protein is available
        totals = {
            "protein": 25
        }

        self.chart.update_chart(totals)

        args, kwargs = self.chart.axis.pie.call_args

        # Protein: 25 * 4 = 100 calories
        # Carbs: 0 calories
        # Fats: 0 calories
        self.assertEqual(
            args[0],
            [100, 0, 0]
        )

        # Verify percentage display
        self.assertEqual(
            kwargs["autopct"],
            "%1.1f%%"
        )

        # Verify the chart is redrawn
        self.chart.canvas.draw_idle.assert_called_once()

    def test_macro_calorie_conversion(self):
        # Verify correct calorie conversion factors
        totals = {
            "protein": 50,
            "carbohydrates": 100,
            "fats": 20
        }

        self.chart.update_chart(totals)

        args, kwargs = self.chart.axis.pie.call_args

        # Protein: 50 * 4 = 200
        # Carbs: 100 * 4 = 400
        # Fats: 20 * 9 = 180
        expected = [200, 400, 180]

        for actual, expected_value in zip(
            args[0],
            expected
        ):
            self.assertAlmostEqual(
                actual,
                expected_value,
                places=2
            )

    def test_negative_macros(self):
        # Negative values should be treated as zero
        totals = {
            "protein": -10,
            "carbohydrates": 50,
            "fats": -5
        }

        self.chart.update_chart(totals)

        args, kwargs = self.chart.axis.pie.call_args

        # Negative protein and fats become zero
        self.assertEqual(
            args[0],
            [0, 200, 0]
        )

    def test_chart_layout_updated(self):
        # Verify layout updates after drawing
        totals = {
            "protein": 100,
            "carbohydrates": 100,
            "fats": 50
        }

        self.chart.update_chart(totals)

        self.chart.axis.clear.assert_called_once()
        self.chart.figure.tight_layout.assert_called_once()
        self.chart.canvas.draw_idle.assert_called_once()


if __name__ == "__main__":
    unittest.main()
