from typing import List

from fastapi import FastAPI, HTTPException

from src.entrypoints import schemas
from src.service_layer import csv_uow, services

app = FastAPI()

uow = csv_uow.CsvUnitOfWork()


@app.post("/products/", status_code=201, response_model=schemas.Product)
async def add_product_endpoint(product: schemas.ProductCreate):
    try:
        services.add_product(
            product.sku,
            product.name,
            product.description,
            product.price,
            product.brand,
            product.category,
            product.stock,
            uow,
        )
    except services.InvalidSku as e:
        raise HTTPException(status_code=400, detail=str(e))
    return services.get_product(product.sku, uow)


@app.get("/products/{sku}", response_model=schemas.Product)
async def get_product_endpoint(sku: str):
    try:
        product = services.get_product(sku, uow)
    except services.ProductNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    return product


@app.get("/products/", response_model=List[schemas.Product])
async def list_products_endpoint():
    return services.list_products(uow)
