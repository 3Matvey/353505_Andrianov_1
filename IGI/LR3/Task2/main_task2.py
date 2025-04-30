"""
Lab #3 - Task 2
Program Name: Summation of Squares
Version: 1.0
Developer: Matvey Andrianov
Date: 2025-04-09

Purpose:
This module implements a loop that reads integer values from the keyboard
and accumulates the sum of their squares. The loop ends when the user enters 0.
"""
from .sum_of_squares import sum_of_squares

def main_task2():
    """
    Main function for Task 2.
    
    This function repeatedly:
     - Welcomes the user to Task 2.
     - Calls `sum_of_squares()` to read numbers and compute their squares' sum.
     - Prints the result.
     - Asks the user if they want to repeat the process or exit.
     
    The function returns when the user chooses to exit.
    """
    while True:
        print("\n=== Task 2: Summation of squares of integers (enter 0 to stop) ===")
        
        result = sum_of_squares()
        print(f"\nThe sum of the squares of the entered numbers is: {result}")

        choice = input("Do you want to repeat Task 2? (y/n): ").strip().lower()
        if choice != 'y':
            print("Exiting Task 2. Goodbye!")
            break

