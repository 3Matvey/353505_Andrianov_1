class ExportRecord:
    """
    Представляет одну запись об экспорте товара:
    название товара, страна-импортер, объем поставки (шт.).
    """
    def __init__(self, product_name: str, country: str, volume: int):
        self.product_name = product_name
        self.country = country
        self.volume = volume

    def __str__(self):
        return f"{self.product_name} → {self.country}: {self.volume}"
