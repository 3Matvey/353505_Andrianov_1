import random

def input_float_list() -> list:
    """
    Repeatedly prompt the user for floating-point numbers to fill a list.
    The user will specify how many numbers to input. If the user enters something invalid, 
    prompt again.

    Returns:
        list: A list of float values entered by the user.
    """
    lst = []
    while True:
        n_str = input("How many elements do you want to input? ")
        try:
            n = int(n_str)
            if n < 0:
                print("Number of elements cannot be negative. Try again.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    for i in range(n):
        while True:
            val_str = input(f"Enter element {i+1}/{n}: ")
            try:
                val = float(val_str)
                lst.append(val)
                break
            except ValueError:
                print("Invalid input. Please enter a valid float number.")
    return lst


def generate_float_list() -> list:
    """
    Generate a list of float numbers automatically (e.g., random or simple sequence).
    The user specifies how many numbers to generate.

    Returns:
        list: A list of float values (in this example, random floats).
    """
    while True:
        n_str = input("How many random elements do you want to generate? ")
        try:
            n = int(n_str)
            if n < 0:
                print("Number of elements cannot be negative. Try again.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
    
    lst = [random.uniform(-10.0, 10.0) for _ in range(n)]
    print(f"Generated list: {lst}")
    return lst
