ADR 0002: Calculate Macronutrients Based on Food Weight

## Status
Accepted

## Context
Users need the ability to enter the weight of a food in grams and automatically calculate its calories and macronutrients. 
The USDA FoodData Central database provides nutritional information for foods, typically based on a 100-gram serving. 
Users should be able to select a food from the USDA search results, enter their desired weight, and view the adjusted nutritional values.

## Decision
We will implement a feature that allows users to enter a food's weight in grams after selecting it from the USDA database. 
The FoodService will calculate the calories, protein, carbohydrates, and fats based on the entered weight using the formula:
Adjusted Nutritional Value = (Food Weight / 100) × Nutritional Value per 100g
The application will display the calculated nutritional information to the user. Input validation will ensure that the entered weight is a positive number.

## Consequences
Allows users to accurately track calories and macronutrients based on the actual amount of food consumed rather than a fixed serving size. 
This improves the application's flexibility and usability. However, the calculations depend on the accuracy of the USDA nutritional data and the weight entered by the user. 
Additional unit tests, such as test_macro_calculations.py, are needed to verify that calculations are performed correctly for different food weights.
