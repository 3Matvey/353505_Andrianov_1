import os
import sys

# чтобы модули export_manager и export_record находились в пути
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from export_manager import ExportManager
from export_record import ExportRecord

def main():
    mgr = ExportManager()

    # --- 1) Добавим исходные данные вручную (словарь можно преобразовать в такие записи) ---
    mgr.add_record(ExportRecord("Телевизоры", "Германия", 120))
    mgr.add_record(ExportRecord("Телевизоры", "Франция", 80))
    mgr.add_record(ExportRecord("Радио",     "Италия",   200))
    mgr.add_record(ExportRecord("Радио",     "Испания",  150))

    # --- 2) Сериализуем в CSV и обратно ---
    mgr.save_to_csv("exports.csv")
    mgr.load_from_csv("exports.csv")

    # --- 3) Сериализуем в pickle и обратно ---
    mgr.save_to_pickle("exports.pkl")
    mgr.load_from_pickle("exports.pkl")

    # --- 4) Поиск по названию товара, список стран и общий объем ---
    product = input("Введите название товара для просмотра экспорта: ")

    countries = mgr.get_countries_by_product(product)
    if not countries:
        print(f"Нет записей об экспорте товара «{product}».")
        return

    print(f"Товар «{product}» экспортируется в следующие страны:")
    for c in countries:
        print(" –", c)

    total = mgr.get_total_volume_by_product(product)
    print(f"Общий объём экспорта: {total} шт.")

if __name__ == "__main__":
    main()
