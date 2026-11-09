ADR 0005: Implement User Login and Registration System

## Status
Completed

## Context
Users need the ability to create personal accounts and securely log into the calorie tracking application. 
Previously, the application allowed users to search for foods and calculate nutritional information without requiring authentication. 
As the application expanded to include daily food logs, it became necessary to associate saved food entries with individual users and prevent users from accessing another user's nutritional data.

## Decision
We will implement a login and registration system using a separate LoginGUI class in the presentation layer. 
Users will be able to register with a username, email, and password or log into an existing account using their credentials. 
An AuthController will communicate with AuthService to validate login information and handle account registration. 
Passwords will be securely hashed using Argon2 before being stored in the SQLite database through UserRepository. 
After successful authentication, the application will open the main calorie tracker interface and pass the authenticated user's information to the food logging services.

## Consequences
Allows users to create personal accounts and securely access their individual food logs. Password hashing improves security by preventing passwords from being stored in plain text. 
Separating authentication into presentation, controller, service, and repository layers supports the application's n-tier architecture and improves maintainability. 
However, the implementation introduces additional complexity involving password validation, database management, authentication errors, and user-specific data access. 
dditional testing is required to ensure registration, login, and account separation function correctly.
