"""
Lab #3 - Task 5
Program Name: Processing a list of real numbers
Version: 1.0
Developer: Your Name
Date: 2025-04-09

Purpose:
This module demonstrates the following functionality for a list of real (float) numbers:
  1) Input of the list from the user (manual input) or via a generator function.
  2) Validation of the input data.
  3) Finding the sum of all negative elements.
  4) Finding the product of elements located between the minimal and the maximal elements (exclusive).
  5) Displaying the results and the list itself.
"""

from .list_initialization import input_float_list, generate_float_list
from .utils import sum_negative_elements, product_between_min_max


def main_task5():
    """
    Main function for Task 5.
    It allows the user to create a list of float numbers either by manual input or via generation,
    then calculates and displays:
      - The sum of negative elements
      - The product of the elements between the minimum and maximum elements
      - The full list
    The user can repeat or exit the task.
    """
    while True:
        print("\n=== Task 5: Processing a list of real numbers ===")
        print("1) Manual input")
        print("2) Automatic generation")
        choice = input("Choose initialization method (1/2): ").strip()

        if choice == '1':
            numbers = input_float_list()
        else:
            numbers = generate_float_list()

        # Display the list to the user
        print(f"\nYour list: {numbers}")

        # Calculate the sum of negative elements
        sum_neg = sum_negative_elements(numbers)
        print(f"Sum of negative elements: {sum_neg}")

        # Calculate the product of elements between min and max
        prod_between = product_between_min_max(numbers)
        print(f"Product of elements between min and max: {prod_between}")

        # Ask if user wants to repeat
        again = input("\nDo you want to run Task 5 again? (y/n): ").strip().lower()
        if again != 'y':
            print("Exiting Task 5. Goodbye!")
            break

