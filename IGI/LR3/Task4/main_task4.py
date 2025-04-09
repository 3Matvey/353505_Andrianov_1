"""
Lab #3 - Task 4
Program Name: Text Analysis (No Regular Expressions)
Version: 1.0
Developer: Matvey Andrianov
Date: 2025-04-09

Purpose:
Given a string of text where words are separated by spaces and commas,
perform the following operations without using any regular expressions:
  1) Count the number of words in the string.
  2) Find the longest word and its position (1-based index).
  3) Print every even-numbered word (2nd, 4th, 6th, etc.).
"""
from .analyze_text import analyze_text

def main_task4():
    """
    Main function for Task 4.
    Demonstrates the text analysis on a predefined string (no regex).
    
    The function:
      - Holds an example text in a string variable.
      - Calls analyze_text(text).
      - Then prompts whether the user wants to analyze another text or exit.
    """
    while True:
        example_text = (
            "She was considering in her own mind, as well as she could, "
            "for the hot day made her feel very sleepy and stupid, whether "
            "the pleasure of making a daisy-chain would be worth the trouble "
            "of getting up and picking the daisies, when suddenly a White "
            "Rabbit with pink eyes ran close by her"
        )

        print("\n=== Task 4: Text Analysis (No Regular Expressions) ===")
        analyze_text(example_text)

        choice = input("\nDo you want to analyze again? (y/n): ").strip().lower()
        if choice != 'y':
            print("Exiting Task 4. Goodbye!")
            break

