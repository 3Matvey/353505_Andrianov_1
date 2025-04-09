"""
Lab #3 - Task 3
Program Name: Count Uppercase English Letters
Version: 1.0
Developer: Your Name
Date: 2025-04-09

Purpose:
This module reads a line of text from the keyboard and counts the number of
uppercase (A-Z) English letters, without using regular expressions.
"""
from .count_uppercase import count_uppercase_en_letters

def main_task3():
    """
    Main function for Task 3.
    It repeatedly prompts the user to input a line of text, counts the number
    of uppercase English letters, and displays the result.
    The user can choose to repeat or exit.
    """
    while True:
        print("\n=== Task 3: Count uppercase English letters ===")
        text = input("Enter a line of text: ")

        uppercase_count = count_uppercase_en_letters(text)
        print(f"\nThere are {uppercase_count} uppercase English letters in the input.")

        choice = input("Do you want to analyze another line? (y/n): ").strip().lower()
        if choice != 'y':
            print("Exiting Task 3. Goodbye!")
            break

