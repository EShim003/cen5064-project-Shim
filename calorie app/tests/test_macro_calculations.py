
import unittest

from service.macro_calculator import MacroCalculator


class TestMacroCalculations(unittest.TestCase):

    def setUp(self):
        self.macros = {
            "calories": 200,
            "protein": 20,
            "carbohydrates": 15,
            "fats": 8
        }

    def test_calculate_macros_100g(self):
        result = MacroCalculator.calculate(self.macros, 100)

        self.assertEqual(result["calories"], 200)
        self.assertEqual(result["protein"], 20)
        self.assertEqual(result["carbohydrates"], 15)
        self.assertEqual(result["fats"], 8)

    def test_calculate_macros_150g(self):
        result = MacroCalculator.calculate(self.macros, 150)

        self.assertEqual(result["calories"], 300)
        self.assertEqual(result["protein"], 30)
        self.assertEqual(result["carbohydrates"], 22.5)
        self.assertEqual(result["fats"], 12)

    def test_calculate_macros_zero_grams(self):
        result = MacroCalculator.calculate(self.macros, 0)

        self.assertEqual(result["calories"], 0)
        self.assertEqual(result["protein"], 0)


if __name__ == "__main__":
    unittest.main()
