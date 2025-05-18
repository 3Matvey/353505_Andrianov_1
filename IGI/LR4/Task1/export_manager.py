import csv
import pickle
from typing import List
from export_record import ExportRecord

class ExportManager:
    """
    Класс для хранения и обработки списка ExportRecord:
    сериализация в CSV и pickle, чтение, поиск, сортировка.
    """
    def __init__(self):
        self.records: List[ExportRecord] = []

    def add_record(self, record: ExportRecord):
        self.records.append(record)

    def save_to_csv(self, filename: str):
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Product", "Country", "Volume"])
                for r in self.records:
                    writer.writerow([r.product_name, r.country, r.volume])
        except Exception as e:
            print(f"Error saving to CSV: {e}")

    def load_from_csv(self, filename: str):
        try:
            with open(filename, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader, None)  # пропустить заголовок
                self.records = [
                    ExportRecord(row[0], row[1], int(row[2]))
                    for row in reader
                ]
        except Exception as e:
            print(f"Error loading from CSV: {e}")

    def save_to_pickle(self, filename: str):
        try:
            with open(filename, 'wb') as f:
                pickle.dump(self.records, f)
        except Exception as e:
            print(f"Error saving to pickle: {e}")

    def load_from_pickle(self, filename: str):
        try:
            with open(filename, 'rb') as f:
                self.records = pickle.load(f)
        except Exception as e:
            print(f"Error loading from pickle: {e}")

    def find_records_by_product(self, product_name: str) -> List[ExportRecord]:
        return [
            r for r in self.records
            if r.product_name.lower() == product_name.lower()
        ]

    def get_countries_by_product(self, product_name: str) -> List[str]:
        recs = self.find_records_by_product(product_name)
        return sorted({r.country for r in recs})

    def get_total_volume_by_product(self, product_name: str) -> int:
        recs = self.find_records_by_product(product_name)
        return sum(r.volume for r in recs)
