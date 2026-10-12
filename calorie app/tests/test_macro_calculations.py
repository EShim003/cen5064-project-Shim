
import unittest

from main import calculate_macros, format_nutrient


class TestMacroCalculations(unittest.TestCase):

    def setUp(self):
        # Example USDA nutrition values per 100 grams
        self.macros = {
            "name": "Bananas, raw",
            "calories": 89,
            "protein": 1.09,
            "carbohydrates": 22.84,
            "fats": 0.33
        }

    def test_macros_for_100_grams(self):
        # 100 grams should return the original USDA values
        result = calculate_macros(self.macros, 100)

        self.assertAlmostEqual(result["calories"], 89)
        self.assertAlmostEqual(result["protein"], 1.09)
        self.assertAlmostEqual(result["carbohydrates"], 22.84)
        self.assertAlmostEqual(result["fats"], 0.33)

    def test_macros_for_150_grams(self):
        # 150 grams should multiply values by 1.5
        result = calculate_macros(self.macros, 150)

        self.assertAlmostEqual(result["calories"], 133.5)
        self.assertAlmostEqual(result["protein"], 1.635)
        self.assertAlmostEqual(result["carbohydrates"], 34.26)
        self.assertAlmostEqual(result["fats"], 0.495)

    def test_macros_for_50_grams(self):
        # 50 grams should multiply values by 0.5
        result = calculate_macros(self.macros, 50)

        self.assertAlmostEqual(result["calories"], 44.5)
        self.assertAlmostEqual(result["protein"], 0.545)
        self.assertAlmostEqual(result["carbohydrates"], 11.42)
        self.assertAlmostEqual(result["fats"], 0.165)

    def test_missing_nutrient(self):
        # Missing USDA values should remain None
        self.macros["fats"] = None

        result = calculate_macros(self.macros, 150)

        self.assertIsNone(result["fats"])
        self.assertAlmostEqual(result["calories"], 133.5)

    def test_nutrient_formatting(self):
        # Nutritional values should display two decimals
        self.assertEqual(
            format_nutrient(133.5, "kcal"),
            "133.50 kcal"
        )

        self.assertEqual(
            format_nutrient(1.635, "g"),
            "1.64 g"
        )

    def test_missing_nutrient_formatting(self):
        # Missing values should display Not available
        self.assertEqual(
            format_nutrient(None, "g"),
            "Not available"
        )


if __name__ == "__main__":
    unittest.main()
