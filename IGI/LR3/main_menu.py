"""
Main Entry Point for Multi-Task Program (Lab 3)
Version: 1.0
Developer: Matvey Andrianov
Date: 2025-04-09

Description:
This module provides a user-friendly menu for choosing one of the five tasks to run.
Task 1 is implemented in the 'Task1' folder (main_task1.py). The other tasks are integrated from their
respective folders with the following functionality:
  - Task 2: Calculate the sum of the squares of integers.
  - Task 3: Count the uppercase English letters in a text string.
  - Task 4: Analyze text by counting the words, finding the longest word along with its position,
            and displaying every even-numbered word.
  - Task 5: Process a list of numbers by summing the negative values and calculating the product of 
            the elements located between the minimum and maximum values.
"""

from Task1.main_task1 import main_task1
from Task2.main_task2 import main_task2
from Task3.main_task3 import main_task3
from Task4.main_task4 import main_task4
from Task5.main_task5 import main_task5

def main_menu():
    """
    Main menu to select one of the five tasks.
    The corresponding function is called based on the selected task.
    """
    while True:
        print("\nSelect a task to run:")
        print("1: Task 1 - Compute sin(x) using power series expansion")
        print("2: Task 2 - Calculate the sum of squares of integers")
        print("3: Task 3 - Count uppercase English letters in a text string")
        print("4: Task 4 - Analyze text: count words, find the longest word, and display even-numbered words")
        print("5: Task 5 - Process a list of numbers: sum negatives and compute product between min and max")
        print("0: Exit the program")

        choice = input("Enter the task number: ").strip()

        if choice == '1':
            main_task1()
        elif choice == '2':
            main_task2()
        elif choice == '3':
            main_task3()
        elif choice == '4':
            main_task4()
        elif choice == '5':
            main_task5()
        elif choice == '0':
            print("Exiting the program.")
            break
        else:
            print("Invalid input. Please enter a number between 0 and 5.")

if __name__ == "__main__":
    main_menu()
