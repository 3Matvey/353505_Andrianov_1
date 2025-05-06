def get_user_choice(quantity : int) -> int:
    while True:
        try:
            choise = int(input(f"Enter your choise (0-{quantity}): "))
            if 0 <= choise <= quantity:
                return choise
            print(f"Please enter a number between 0 and {quantity}")
        except ValueError:
            print("Please enter a valid number")
