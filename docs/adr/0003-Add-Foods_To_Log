ADR 0003: Allow Users to Add Searched Foods to Their Daily Food Log

## Status
Completed

## Context
Users need the ability to save foods they find through the USDA food search feature instead of only viewing their nutritional information. 
The application should allow users to enter the amount of food consumed and track their total daily calories, protein, carbohydrates, and fats.

## Decision
We will implement a FoodLogService that allows users to add searched foods to their daily food log. 
The service will use the existing MacroCalculator to calculate nutritional values based on the entered weight. 
A FoodLogRepository will store food entries in SQLite and associate them with the logged-in user and date. 
The application will automatically calculate daily nutritional totals and allow users to remove previously logged foods.

## Consequences
Allows users to track their daily food consumption and monitor their total calorie and macronutrient intake. Food entries are saved between application sessions and associated with individual users.
However, the implementation introduces additional database operations, validation requirements, and testing to ensure accurate nutritional calculations and data persistence.
