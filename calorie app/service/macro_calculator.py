
class MacroCalculator:

    @staticmethod
    def calculate(macros, grams):
        """Calculate nutrients for a specified weight in grams."""

        multiplier = grams / 100

        return {
            "calories": (
                macros["calories"] * multiplier
                if macros["calories"] is not None else None
            ),
            "protein": (
                macros["protein"] * multiplier
                if macros["protein"] is not None else None
            ),
            "carbohydrates": (
                macros["carbohydrates"] * multiplier
                if macros["carbohydrates"] is not None else None
            ),
            "fats": (
                macros["fats"] * multiplier
                if macros["fats"] is not None else None
            )
        }
