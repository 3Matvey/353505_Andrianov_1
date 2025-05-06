"""
Task 1: Export Data Management System
This module provides the main interface for managing export data.
"""

from .models import ExportRecord, ExportData
from .utils import CSVSerializer, PickleSerializer
from common.user_input import get_user_choice

def display_menu():
    """Display the main menu for task 1."""
    print("\n=== Export Data Management System ===")
    print("1. Add new export record")
    print("2. Search for product information")
    print("3. Save data to CSV")
    print("4. Load data from CSV")
    print("5. Save data to Pickle")
    print("6. Load data from Pickle")
    print("0. Return to main menu")
    print("===================================")


def display_available_products(data: ExportData):
    """Display a list of all available products in the storage."""
    products = set(record.product_name for record in data)
    if not products:
        print("\nNo products in the storage.")
        return
    
    print("\nAvailable products in the storage:")
    for i, product in enumerate(sorted(products), 1):
        print(f"{i}. {product}")

def add_record(data: ExportData):
    """Add a new export record."""
    try:
        product = input("Enter product name: ").strip()
        country = input("Enter importing country: ").strip()
        quantity = int(input("Enter quantity: "))
        
        if not product or not country or quantity <= 0:
            print("Invalid input. All fields are required and quantity must be positive.")
            return
        
        record = ExportRecord(product, country, quantity)
        data.add_record(record)
        print("Record added successfully!")
    except ValueError:
        print("Invalid quantity. Please enter a positive number.")

def search_product(data: ExportData):
    """Search for product information."""
    product = input("Enter product name to search: ").strip()
    if not product:
        print("Product name cannot be empty.")
        return
    
    countries = data.get_countries_by_product(product)
    total_quantity = data.get_total_export_quantity(product)
    
    if not countries:
        print(f"No export records found for product: {product}")
        return
    
    print(f"\nExport information for {product}:")
    print(f"Importing countries: {', '.join(countries)}")
    print(f"Total export quantity: {total_quantity}")
    
    print("\nDetailed records:")
    for record in data.get_product_info(product):
        print(record)

def save_to_csv(data: ExportData):
    """Save data to CSV file."""
    filename = input("Enter filename to save (without extension): ").strip()
    if not filename:
        print("Filename cannot be empty.")
        return
    
    try:
        CSVSerializer.save_data(data, f"{filename}.csv")
        print("Data saved successfully to CSV file.")
    except Exception as e:
        print(f"Error saving data: {e}")

def load_from_csv(data: ExportData):
    """Load data from CSV file."""
    filename = input("Enter filename to load (without extension): ").strip()
    if not filename:
        print("Filename cannot be empty.")
        return
    
    try:
        loaded_data = CSVSerializer.load_data(f"{filename}.csv")
        data._records = loaded_data._records
        print("Data loaded successfully from CSV file.")
        display_available_products(data)
    except Exception as e:
        print(f"Error loading data: {e}")

def save_to_pickle(data: ExportData):
    """Save data to pickle file."""
    filename = input("Enter filename to save (without extension): ").strip()
    if not filename:
        print("Filename cannot be empty.")
        return
    
    try:
        PickleSerializer.save_data(data, f"{filename}.pkl")
        print("Data saved successfully to pickle file.")
    except Exception as e:
        print(f"Error saving data: {e}")

def load_from_pickle(data: ExportData):
    """Load data from pickle file."""
    filename = input("Enter filename to load (without extension): ").strip()
    if not filename:
        print("Filename cannot be empty.")
        return
    
    try:
        loaded_data = PickleSerializer.load_data(f"{filename}.pkl")
        data._records = loaded_data._records
        print("Data loaded successfully from pickle file.")
        display_available_products(data)
    except Exception as e:
        print(f"Error loading data: {e}")

def main():
    """Main function for task 1."""
    data = ExportData()
    
    while True:
        display_menu()
        choice = get_user_choice(6)
        
        if choice == 0:
            break
        elif choice == 1:
            add_record(data)
        elif choice == 2:
            search_product(data)
        elif choice == 3:
            save_to_csv(data)
        elif choice == 4:
            load_from_csv(data)
        elif choice == 5:
            save_to_pickle(data)
        elif choice == 6:
            load_from_pickle(data)

if __name__ == "__main__":
    main() 