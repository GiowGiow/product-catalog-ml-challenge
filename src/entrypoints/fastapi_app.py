from typing import List

from fastapi import Depends, FastAPI, HTTPException

from src.entrypoints import schemas
from src.service_layer import csv_uow, services, unit_of_work

app = FastAPI()


def get_uow():
    return csv_uow.CsvUnitOfWork()


@app.post("/products/", status_code=201, response_model=schemas.Product)
async def add_product_endpoint(
    product_data: schemas.ProductCreate,
    uow: unit_of_work.AbstractUnitOfWork = Depends(get_uow),
):
    try:
        product = services.add_product(
            product_data.sku,
            product_data.name,
            product_data.description,
            product_data.price,
            product_data.brand,
            product_data.category,
            product_data.stock,
            uow,
        )
    except services.InvalidSku as e:
        raise HTTPException(status_code=400, detail=str(e))
    return product


@app.get("/products/{sku}", response_model=schemas.Product)
async def get_product_endpoint(
    sku: str, uow: unit_of_work.AbstractUnitOfWork = Depends(get_uow)
):
    try:
        product = services.get_product(sku, uow)
    except services.ProductNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    return product


@app.get("/products/", response_model=List[schemas.Product])
async def list_products_endpoint(
    uow: unit_of_work.AbstractUnitOfWork = Depends(get_uow),
):
    return services.list_products(uow)
