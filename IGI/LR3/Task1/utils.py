"""
Module: utils
Purpose: Contains utility functions such as decorators and input validation functions.
"""

def repeat_program(func):
    """
    Decorator to allow the wrapped function to be repeated based on user input.
    
    After the decorated function completes, it asks whether the user would like to run it again.
    
    Parameters:
        func (function): The function to be executed repeatedly.
    
    Returns:
        function: The wrapped function.
    """
    def wrapper(*args, **kwargs):
        while True:
            func(*args, **kwargs)
            again = input("Do you want to perform another calculation? (y/n): ").strip().lower()
            if again != 'y':
                print("Exiting program. Goodbye!")
                break
    return wrapper

def safe_input_float(prompt: str) -> float:
    """
    Prompt the user for a float input and validate the input.

    Parameters:
        prompt (str): The input prompt displayed to the user.
    
    Returns:
        float: The user-inputted float value.
    """
    while True:
        try:
            value_str = input(prompt)
            value = float(value_str)
            return value
        except ValueError:
            print("Invalid input. Please enter a valid float number.")

def safe_input_int(prompt: str) -> int:
    """
    Prompt the user for an integer input and validate the input.

    Parameters:
        prompt (str): The input prompt displayed to the user.
    
    Returns:
        int: The user-inputted integer value.
    """
    while True:
        try:
            value_str = input(prompt)
            value = int(value_str)
            return value
        except ValueError:
            print("Invalid input. Please enter a valid integer number.")
