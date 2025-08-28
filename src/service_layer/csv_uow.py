from src.adapters import repository
from src.service_layer import unit_of_work


class CsvUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(self, filepath: str = "data/products.csv"):
        self.products = repository.CsvRepository(filepath)
        self._filepath = filepath

    def commit(self):
        pass

    def rollback(self):
        pass
