def sum_of_squares() -> int:
    """
    Continuously read integers from the user and sum their squares.
    The loop ends upon reading the integer 0.
    
    Returns:
        int: The sum of squares of all entered integers except 0.
    Raises:
        ValueError: This function does not raise ValueError by itself,
                    but it handles any invalid input from the user by
                    prompting again.
    """
    total = 0
    while True:
        user_input = input("Enter an integer (0 to stop): ")

        try:
            number = int(user_input)
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
            continue

        if number == 0:
            break

        total += number * number

    return total

