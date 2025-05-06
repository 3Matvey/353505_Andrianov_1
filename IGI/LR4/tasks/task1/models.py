"""
Task 1: Export Data Management
This module contains classes for handling export data operations.
"""

class ExportRecord:
    """Class representing a single export record."""
    
    def __init__(self, product_name: str, country: str, quantity: int):
        """
        Initialize an export record.
        
        Args:
            product_name (str): Name of the exported product
            country (str): Importing country
            quantity (int): Quantity of products in the shipment
        """
        self._product_name = product_name
        self._country = country
        self._quantity = quantity
    
    @property
    def product_name(self) -> str:
        """Get the product name."""
        return self._product_name
    
    @property
    def country(self) -> str:
        """Get the importing country."""
        return self._country
    
    @property
    def quantity(self) -> int:
        """Get the quantity of products."""
        return self._quantity
    
    def __str__(self) -> str:
        """String representation of the export record."""
        return f"Product: {self._product_name}, Country: {self._country}, Quantity: {self._quantity}"

class ExportData:
    """Class for managing export data operations."""
    
    def __init__(self):
        """Initialize the export data manager."""
        self._records = []
    
    def add_record(self, record: ExportRecord) -> None:
        """
        Add a new export record.
        
        Args:
            record (ExportRecord): The record to add
        """
        self._records.append(record)
    
    def get_countries_by_product(self, product_name: str) -> list:
        """
        Get all countries importing a specific product.
        
        Args:
            product_name (str): Name of the product
            
        Returns:
            list: List of countries importing the product
        """
        return [record.country for record in self._records 
                if record.product_name.lower() == product_name.lower()]
    
    def get_total_export_quantity(self, product_name: str) -> int:
        """
        Calculate total export quantity for a specific product.
        
        Args:
            product_name (str): Name of the product
            
        Returns:
            int: Total quantity exported
        """
        return sum(record.quantity for record in self._records 
                  if record.product_name.lower() == product_name.lower())
    
    def get_product_info(self, product_name: str) -> list:
        """
        Get all export records for a specific product.
        
        Args:
            product_name (str): Name of the product
            
        Returns:
            list: List of ExportRecord objects
        """
        return [record for record in self._records 
                if record.product_name.lower() == product_name.lower()]
    
    def __iter__(self):
        """Make the class iterable."""
        return iter(self._records) 