ADR 0006: Add Pie Chart and Enhanced Visuals for Calorie Tracker UI

## Status
Completed

## Context
Users need a clear and visually appealing way to understand their daily calorie and macronutrient intake. 
Previously, the application displayed nutritional information primarily through text, showing calories, protein, carbohydrates, and fats in grams.
As the application expanded to include daily food logs and nutritional totals, it became beneficial to provide a visual representation of the user's macronutrient breakdown. 
This would allow users to quickly understand the percentage of their daily intake coming from protein, carbohydrates, and fats without manually calculating the percentages.

## Decision
We will enhance the calorie tracker interface by implementing a pie chart using the Matplotlib library. 
A separate MacroPieChart class will be created in the presentation layer to handle chart creation and updates.
The pie chart will display the percentage of calories contributed by each macronutrient rather than simply displaying the total grams. 
Protein and carbohydrates will be calculated using 4 calories per gram, while fats will use 9 calories per gram.
The chart will use different colors to distinguish macronutrients: blue for protein, yellow for carbohydrates, and green for fats.
The chart will automatically update whenever users add or remove foods from their daily food log. 
The interface will also be enhanced to provide a clearer presentation of nutritional totals and logged food entries.

## Consequences
Allows users to better visualize their daily macronutrient intake and understand the percentage of calories coming from protein, carbohydrates, and fats. 
The enhanced interface improves readability and makes nutritional information easier to interpret.
Separating chart functionality into its own MacroPieChart class supports the Single Responsibility Principle and improves maintainability 
by keeping visualization logic separate from food logging and nutritional calculations.
However, implementing the chart introduces an additional dependency on Matplotlib and increases the complexity of the graphical interface. 
Additional testing is required to ensure percentages are calculated correctly, charts update when food entries change, and empty food logs are handled without errors.
