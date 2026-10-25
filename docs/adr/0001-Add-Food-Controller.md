ADR 0001: Allow Users to Add Custom Foods

## Status
Accepted

## Context
Users need the ability to add their own foods to the calorie tracking application when a food is unavailable in the USDA database. 
Users should be able to manually enter a food's name, calories, protein, carbohydrates, and fats to accurately track their daily nutritional intake.

## Decision
We will implement an AddFoodController that communicates with the FoodService to validate and process manually entered food information. 
The application will allow users to enter custom foods with their own calorie and macronutrient values. Input validation will prevent invalid entries, such as negative calories or macronutrients.

## Consequences
Allows users to track foods that are not available in the USDA database, making the application more flexible and customizable.
However, manually entered nutritional information may be inaccurate, and additional validation and testing are required to ensure the application handles invalid inputs correctly.
