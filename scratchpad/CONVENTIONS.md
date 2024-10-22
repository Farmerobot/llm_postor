# Engineering Conventions

## Conventions
> When writing code, it is important to follow conventions to ensure that the code is readable and maintainable. This document outlines the conventions that should be followed when writing code for the project.

- **Write simple, verbose code over terse, dense code.**  Prioritize clarity and readability.  Avoid overly clever or obfuscated code.  For example, prefer `x = x + 1` over `x += 1` if the former is more easily understood in context.

- **If a function does not have a corresponding test, mention it.**  Document why a test is missing (e.g.,  "TODO: Add test for this function.  Currently difficult to test due to [reason]").  This helps track untested code and prioritize testing efforts.

- **Use descriptive variable and function names.**  Names should clearly indicate the purpose of the variable or function.  For example, `calculate_average_score` is better than `calc_avg`.

- **Keep functions concise and focused.**  Each function should ideally perform a single, well-defined task.  Long functions should be broken down into smaller, more manageable units.

- **Use docstrings to document functions and classes.**  Docstrings should clearly explain the purpose, parameters, return values, and any exceptions raised by a function or class.

- **Handle errors gracefully.**  Use `try...except` blocks to catch and handle potential errors, preventing unexpected crashes.  Log errors appropriately for debugging purposes.

- **Write unit tests.**  Thorough unit tests are crucial for ensuring the correctness and maintainability of the code.  Aim for high test coverage.
