import csv
import os
import time

from src.adapters import repository
from src.service_layer import unit_of_work


class CsvUnitOfWork(unit_of_work.AbstractUnitOfWork):
    """
    CSV-based implementation of the Unit of Work pattern.

    This class manages transactions and data persistence for product operations
    using a CSV file as the data store. It implements file locking to ensure
    data consistency in concurrent environments.

    The Unit of Work pattern maintains a list of objects affected by a business
    transaction and coordinates writing out changes and resolving concurrency problems.

    Args:
        filepath (str): Path to the CSV file. Defaults to "data/products.csv".

    Raises:
        TimeoutError: If lock cannot be acquired within 5 seconds.

    Example:
        with CsvUnitOfWork() as uow:
            product = uow.products.get("SKU123")
            product.price = 99.99
            uow.commit()  # Changes are persisted to CSV
    """

    def __init__(self, filepath: str = "data/products.csv"):
        self.products = repository.CsvRepository(filepath)
        self._filepath = filepath
        self._lock_filepath = f"{filepath}.lock"

    def _acquire_lock(self):
        start_time = time.time()
        while True:
            try:
                # Use atomic file creation to acquire the lock
                self._lock_fd = os.open(
                    self._lock_filepath, os.O_CREAT | os.O_EXCL | os.O_WRONLY
                )
                return
            except FileExistsError:
                if time.time() - start_time >= 5:  # 5-second timeout
                    raise TimeoutError(f"Could not acquire lock for {self._filepath}")
                time.sleep(0.1)

    def _release_lock(self):
        if hasattr(self, "_lock_fd"):
            os.close(self._lock_fd)
            os.remove(self._lock_filepath)

    def __enter__(self):
        self._acquire_lock()
        self.products = repository.CsvRepository(self._filepath)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self._release_lock()

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
