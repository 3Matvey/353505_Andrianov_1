"""
Lab 1 - Series Expansion Calculation for sin(x)
Program Version: 1.0
Developer: Your Name (Replace with your full name)
Date of Development: 2025-04-09

Description:
This program calculates the value of sin(x) using its power series expansion method.
The user is prompted for the precision (epsilon) and can also initialize a sequence of x values
either via manual input or using a generator (an arithmetic progression in this example).
For each x value, the program displays the computed series approximation, the actual math.sin(x) value,
the absolute error, and the number of terms used to achieve the specified precision.
The program supports repeated calculations without exiting.
"""

import math
from .series_functions import calculate_sin_series
from .init_functions import init_sequence_generator, init_sequence_input
from .utils import repeat_program, safe_input_float, safe_input_int

@repeat_program
def main_task1():
    """
    Main function for executing the series expansion calculations.

    The function prompts the user for the initialization method, sequence length, and precision.
    Then it calculates sin(x) for each x in the sequence using power series expansion and displays the results.
    """
    print("\nWelcome to the sin(x) power series expansion calculator!")
    
    n = safe_input_int("Enter the number of x values you want to calculate: ")
    
    print("\nChoose initialization method for x values:")
    print("1 - Manual input")
    print("2 - Generator (arithmetic progression starting from 0 with step 1)")
    method_choice = input("Enter your choice (1/2): ").strip()
    
    if method_choice == '1':
        x_values = init_sequence_input(n)
    else:
        x_values = init_sequence_generator(n)
        print("Generated x values:", x_values)
    
    eps = safe_input_float("Enter the precision (epsilon) for the calculation (e.g., 0.0001): ")
    
    for x in x_values:
        print(f"\nCalculating sin({x}) using power series expansion...")
        try:
            approx, terms = calculate_sin_series(x, eps)
            actual = math.sin(x)
            error = abs(approx - actual)
            print(f"Approximated sin({x}) = {approx}")
            print(f"Actual sin({x})       = {actual}")
            print(f"Absolute error        = {error}")
            print(f"Number of terms used  = {terms}")
        except Exception as e:
            print(f"An error occurred for x = {x}: {e}")

