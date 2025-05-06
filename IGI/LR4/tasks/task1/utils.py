"""
Task 1: Data Serialization Utilities
This module contains functions for serializing and deserializing export data.
"""

import csv
import pickle
from typing import List, Dict
from abc import ABC, abstractmethod
from .models import ExportRecord, ExportData

class DataSerializer(ABC):
    """Abstract base class for data serialization."""
    
    @staticmethod
    @abstractmethod
    def save_data(data: ExportData, filename: str) -> None:
        """
        Save data to file.
        
        Args:
            data (ExportData): Data to save
            filename (str): Path to the output file
        """
        pass
    
    @staticmethod
    @abstractmethod
    def load_data(filename: str) -> ExportData:
        """
        Load data from file.
        
        Args:
            filename (str): Path to the input file
            
        Returns:
            ExportData: Loaded data
        """
        pass

class CSVSerializer(DataSerializer):
    """CSV format serializer."""
    
    @staticmethod
    def save_data(data: ExportData, filename: str) -> None:
        """
        Save export data to CSV file.
        
        Args:
            data (ExportData): Data to save
            filename (str): Path to the output file
        """
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Product', 'Country', 'Quantity'])
            for record in data:
                writer.writerow([record.product_name, record.country, record.quantity])
    
    @staticmethod
    def load_data(filename: str) -> ExportData:
        """
        Load export data from CSV file.
        
        Args:
            filename (str): Path to the input file
            
        Returns:
            ExportData: Loaded data
        """
        data = ExportData()
        with open(filename, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if len(row) == 3:
                    record = ExportRecord(row[0], row[1], int(row[2]))
                    data.add_record(record)
        return data

class PickleSerializer(DataSerializer):
    """Pickle format serializer."""
    
    @staticmethod
    def save_data(data: ExportData, filename: str) -> None:
        """
        Save export data using pickle.
        
        Args:
            data (ExportData): Data to save
            filename (str): Path to the output file
        """
        with open(filename, 'wb') as file:
            pickle.dump(data, file)
    
    @staticmethod
    def load_data(filename: str) -> ExportData:
        """
        Load export data using pickle.
        
        Args:
            filename (str): Path to the input file
            
        Returns:
            ExportData: Loaded data
        """
        with open(filename, 'rb') as file:
            return pickle.load(file) 