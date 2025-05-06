"""
Lab Work #4: Python Programming
Version: 1.0
Developer: Matvey Andrianov 
Date: 06.05.2025

This program implements five different tasks demonstrating various Python OOP concepts.
Each task showcases different aspects of object-oriented programming including:
- Static and dynamic class attributes
- Polymorphism
- Special (magic) methods
- Inheritance with super()
- Getters and setters
- Class properties
- Mixins
"""
from common.user_input import get_user_choice
from tasks.task1.main import main as task1_main
from tasks.task2.main import main as task2_main
from tasks.task3.main import main as task3_main
from tasks.task4.main import main as task4_main
from tasks.task5.main import main as task5_main

def display_menu():
    """Display the main menu with available tasks."""
    print("\n=== Lab Work #4 Menu ===")
    print("1. Export Data Management System")
    print("2. Text Analysis System")
    print("3. Function Series Analysis and Plotting")
    print("4. Isosceles Triangle Figure OOP Demo")
    print("5. NumPy Matrix Column Median Task")
    print("0. Exit")
    print("=======================")

def main():
    """Main program loop."""
    while True:
        display_menu()
        choice = get_user_choice(5)
        
        if choice == 0:
            print("Goodbye!")
            break
        elif choice == 1:
            task1_main()
        elif choice == 2:
            task2_main()
        elif choice == 3:
            task3_main()
        elif choice == 4:
            task4_main()
        elif choice == 5:
            task5_main()
        else:
            print(f"Task {choice} is not implemented yet.")

if __name__ == "__main__":
    main()
