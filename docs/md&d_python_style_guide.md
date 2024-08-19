# **Introduction**

The Python Coding Style Guide is a vital resource for our development team. It serves as a comprehensive reference for writing clean, consistent, and maintainable Python code. The principles outlined in this guide are designed to enhance the quality of our codebase, promote modularity, improve robustness, and minimize the onboarding time required for new team members.

## **Importance of this Document**

**Maintainability**: Adhering to the coding style and best practices presented in this guide enhances the accessibility and ease of maintaining our codebase. Clear naming conventions, concise comments, and structured organization help us quickly understand and modify code, facilitating long-term maintenance.

**Modularity**: Structuring our code into functions, classes, and organized modules promotes modularity. Modularity increases code reusability, making it easier to extend and adapt our software to changing requirements.

**Robustness**: This guide includes recommendations for proper exception handling, informative error messages, and clear documentation, contributing to the robustness of our code. This enables our code to handle unexpected situations and errors gracefully.

**Reduced Onboarding Time**: Consistency in coding style and organization, along with documentation and transparency, reduces the time required for onboarding. This allows new and existing team members, as well as external collaborators, to engage with the codebase more efficiently and effectively.

# **The Guide**

### **Naming Conventions**

- Use clear and consistent naming conventions:
    - Use snake_case for variable and function names, e.g., `predict_proba()`.
    - Use CamelCase for class names, e.g., `ViewsLoader`.
    - Use UPPERCASE for constants, e.g., `LEARNING_RATE`.

### **String Quotes**

- Use single or double quotes for string literals consistently.
- Prefer single quotes for short strings and double quotes for strings that include single quotes.
- Prefer triple quotes over concatenation or escaping for multi-line strings.
- Use formatted strings (f'...') for output instead of concatenation.

### **Comments and Docstrings**

- Use docstrings to document modules, classes, functions, and methods.
- All classes and functions should contain a docstring, providing context and documentation for the code, its purpose, and usage. Ideally, use either the PyCharm or the VSCode default docstring template.
- Keep comments concise and to the point.
- Write comments in complete sentences and use proper grammar.

### **Imports**

- Follow a clear and organized import structure.
- Use absolute imports whenever possible.
- Wildcard imports (`from module import *`) should be avoided, with two exceptions: Pandas extenders and decorators, i.e., the `ingester` and `views_forecasts` modules, where wildcard imports are the norm (as you want the entire data model). Be explicit about what you are importing.
- Import only the libraries, functions, classes, or variables you need.

### **Function Definitions**

- Use descriptive function names.
- When defining a function, include type hints in the function signatures if needed. There is no need to use type hints everywhere, especially if they obscure the understanding of the code.

```python
def function_name() -> returntype:
```

- Keep functions short and focused on a single task.
- Functions should return a new value and not modify existing data in place. If you need to modify data in place within a function, you MUST use a docstring.
- Never use an empty mutable argument as a default in a function. Always use the `None` type and handle it properly in the code:

```python
# NEVER: 
def function_name(x=[]):
# INSTEAD:
def function_name(x=None):
```

### **Classes**

- Classes should represent objects and encapsulate data/metadata and behavior. Use classes when you need to create complex data structures or complex behavior connected to data, store states, store and process metadata, etc.
- Avoid using classes for simple operations that can be achieved with functions.

### **Configuration and Parameters**

- Do not hardcode parameters, hyperparameters, and configurations directly in your scripts.
- Use dedicated `.py` configuration files, containing Python dictionaries, to store parameters.
- Avoid using config files based on parsed markup languages such as YAML, TOML, or JSON if you can avoid it.

### **Utility Functions and Classes**

- Keep utility functions and classes in dedicated scripts.
- Avoid including them in do-everything scripts.
- Use import statements to access utility functions and classes if needed.
- If software is to be reused in multiple contexts, package it and publish it to **PyPI**. It’s easier than you think, and it’s incredibly easy to automate the production and distribution of the packages completely. We use Poetry and GitHub Actions and have code and expertise in-house.

### **Code Folding Structure**

- Maintain a neat and best-practice folding structure in your code to improve readability.
- Avoid arbitrary changes or expansions of the folding structure.

### **Jupyter Notebooks**

- Use Jupyter notebooks for experimentation, data exploration, and debugging.
- Store Jupyter notebooks in separate folders to keep them organized.
- Notebooks should **never** be part of the production pipeline. Only `.py` files should be used in the production pipeline.

### **Exception Handling**

- Use exception handling (`try`, `except`) blocks in functions where exceptions need to be caught and handled.
- Catch specific exceptions rather than using a broad `except:` clause.
- Always include an error message when raising exceptions.
- Avoid using non-canonical approaches for exception handling and passing, such as monads (e.g., "maybe/just") or other complex data types that encapsulate branching for errors.

### **List Comprehensions**

- Prefer list comprehensions over `for` loops when creating simple data structures programmatically. However, if your list comprehension needs to be split into more than one line of code, use a `for` loop.
- Keep list comprehensions short and readable.

### **Code Organization**

- Organize your code into logical functions, classes, files, and packages (if necessary).
- There should be minimal free-floating code. If there is free-floating code, e.g., runners or argument parsers, don’t forget to include the `if __name__ == '__main__':` clause above the free-floating code. This allows the file to be imported as a package elsewhere without running that code.
- Code should be sorted into modules containing functions and classes to improve structure, reusability, and maintainability.
- Always use a `main()` function in `.py` scripts for reusability of functions within the scripts.
