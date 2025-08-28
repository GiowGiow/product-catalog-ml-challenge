import csv

from src.adapters import repository
from src.service_layer import unit_of_work


class CsvUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(self, filepath: str = "data/products.csv"):
        self.products = repository.CsvRepository(filepath)
        self._filepath = filepath

    def commit(self):
        with open(self._filepath, "w", newline="") as f:
            fieldnames = [
                "sku",
                "name",
                "description",
                "price",
                "brand",
                "category",
                "stock",
                "created_at",
                "updated_at",
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for product in self.products.list():
                writer.writerow(
                    {
                        "sku": product.sku,
                        "name": product.name,
                        "description": product.description,
                        "price": product.price,
                        "brand": product.brand,
                        "category": product.category,
                        "stock": product.stock,
                        "created_at": product.created_at.isoformat(),
                        "updated_at": product.updated_at.isoformat()
                        if product.updated_at
                        else "",
                    }
                )

    def rollback(self):
        pass
