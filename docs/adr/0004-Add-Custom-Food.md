ADR 0004: Add Custom Food Creation into CustomFoodService

## Status
Completed

## Context
Users need the ability to manually add foods with their own calories and macronutrients when those foods are unavailable through USDA search. 
Initially, this functionality was considered for implementation inside FoodLogService. 
However, adding custom food creation and validation responsibilities to the existing service raised concerns about violating the Single Responsibility Principle (SRP) of SOLID design.

## Decision
We will create a separate CustomFoodService class responsible for validating and saving manually entered food information. 
The service will validate food names, weights, calories, protein, carbohydrates, and fats before creating a FoodLog object. 
Both CustomFoodService and FoodLogService will use the existing FoodLogRepository to store entries in SQLite. 
The GUI will provide a separate Add Custom Food window, and main.py will inject the new service into the application.

## Consequences
Improves code organization and maintainability by separating custom food creation from existing food log functionality. 
Supports the Single Responsibility Principle and allows custom food validation to be tested independently. Reusing the existing repository avoids unnecessary database tables. 
However, introducing another service increases the number of application components and requires additional dependency initialization and unit tests.
