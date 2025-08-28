import csv

from src.adapters import repository
from src.service_layer import unit_of_work


class CsvUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(self, filepath: str = "products.csv"):
        self.products = repository.CsvRepository(filepath)
        self._filepath = filepath

    def commit(self):
        with open(self._filepath, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
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
            )
            for p in self.products.list():
                writer.writerow(
                    [
                        p.sku,
                        p.name,
                        p.description,
                        p.price,
                        p.brand,
                        p.category,
                        p.stock,
                        p.created_at.isoformat(),
                        p.updated_at.isoformat() if p.updated_at else "",
                    ]
                )

    def rollback(self):
        pass
