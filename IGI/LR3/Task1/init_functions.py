"""
Module: init_functions
Purpose: Provides functions for initializing sequences based on user input or generators.
"""

def init_sequence_generator(n: int) -> list:
    """
    Initialize a sequence using a generator (example: arithmetic progression).

    Parameters:
        n (int): The number of elements in the sequence.
    
    Returns:
        list: A list of float numbers generated as an arithmetic progression (starting from 0 with a step of 1).
    """
    return [float(i) for i in range(n)]

def init_sequence_input(n: int) -> list:
    """
    Initialize a sequence based on user input.

    Parameters:
        n (int): The number of elements to input.
    
    Returns:
        list: A list of float numbers entered by the user.
    """
    sequence = []
    for i in range(n):
        while True:
            try:
                value_str = input(f"Enter element {i+1}/{n}: ")
                value = float(value_str)
                sequence.append(value)
                break
            except ValueError:
                print("Invalid input. Please enter a valid number.")
    return sequence
