# Engineering Conventions

## Conventions
> When writing code, it is important to follow conventions to ensure that the code is readable and maintainable. This document outlines the conventions that should be followed when writing code for the project.

- Write simple verbose code over terse dense code.
- If a function does not have a corresponding test, mention it.


**Code Style:**

* **Naming:**
    * Use descriptive and consistent naming for variables, functions, classes, and modules.
* **Comments:**
    * Use clear and concise comments to explain complex logic or non-obvious code.
    * Avoid redundant comments that simply restate the code.

**Testing:**

* **Unit Tests:** Write unit tests for all functions and classes to ensure their correctness.
* **Integration Tests:** Write integration tests to verify the interaction between different components of the system.
* **Test Coverage:** Aim for high test coverage to ensure that all code paths are tested.

**Code Organization:**

* **Modules:** Organize code into logical modules to improve maintainability.
* **Classes:** Use classes to encapsulate data and behavior.
* **Functions:** Keep functions small and focused on a single task.
* **Error Handling:** Implement robust error handling to prevent unexpected crashes.

In addition to the SOLID principles, Python code should generally adhere to the following universally recognized guidelines and rules to ensure clarity, maintainability, and efficiency:

### 2. **DRY (Don’t Repeat Yourself)**
   - **Avoid Code Duplication**: Reuse code by creating functions or classes to handle repeated tasks. It makes the code easier to maintain and reduces bugs.
   
### 3. **KISS (Keep It Simple, Stupid)**
   - **Simplicity**: Write code that is simple and straightforward. Complex solutions should be avoided unless absolutely necessary.

### 4. **YAGNI (You Aren't Gonna Need It)**
   - **Avoid Premature Optimization**: Only implement features or optimizations when they are absolutely necessary. Don’t add features "just in case" they’ll be needed in the future.

### 5. **Separation of Concerns**
   - **Modularization**: Organize code into separate, distinct sections (functions, classes, or modules), each handling a specific task. This improves maintainability and scalability.

### 6. **Single Responsibility Principle (SRP)**
   - Similar to SOLID's SRP, this principle suggests that every module or function should have one and only one reason to change, which is its responsibility.

### 7. **Liskov Substitution Principle**
   - Objects of a superclass should be replaceable with objects of a subclass without affecting the correctness of the program.

### 8. **Avoid Side Effects**
   - Functions should be as pure as possible, avoiding changes to variables outside of their scope unless necessary.

### 9. **Error Handling**
   - Use **try/except** blocks wisely to handle exceptions. Ensure your code fails gracefully with meaningful error messages and avoids swallowing exceptions.

### 10. **Use Built-in Functions and Libraries**
   - Python has a rich standard library. Instead of reinventing the wheel, prefer Python’s built-in functions and modules, which are often optimized and well-tested.

### 11. **Testing and Documentation**
   - Write **unit tests** for your code to ensure its functionality.
   - Keep your code **well-documented** for future developers or your future self.

These rules help Python developers write clean, maintainable, and efficient code that follows widely accepted conventions.

Remember, the goal of conventions is to make this code more readable, maintainable, and collaborative.