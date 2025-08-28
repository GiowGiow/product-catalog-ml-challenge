from typing import List

from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader

from src.entrypoints import schemas
from src.service_layer import csv_uow, services, unit_of_work

app = FastAPI()

API_KEY = "your-secret-api-key"
API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)


async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return api_key


def get_uow():
    return csv_uow.CsvUnitOfWork()


@app.post("/products/", status_code=201, response_model=schemas.Product)
async def add_product_endpoint(
    product_data: schemas.ProductCreate,
    uow: unit_of_work.AbstractUnitOfWork = Depends(get_uow),
    api_key: str = Depends(get_api_key),
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


@app.put("/products/{sku}", response_model=schemas.Product)
async def edit_product_endpoint(
    sku: str,
    product_data: schemas.ProductUpdate,
    uow: unit_of_work.AbstractUnitOfWork = Depends(get_uow),
    api_key: str = Depends(get_api_key),
):
    try:
        product = services.edit_product(
            sku, product_data.model_dump(exclude_unset=True), uow
        )
    except services.ProductNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    return product


@app.delete("/products/{sku}", status_code=204)
async def remove_product_endpoint(
    sku: str,
    uow: unit_of_work.AbstractUnitOfWork = Depends(get_uow),
    api_key: str = Depends(get_api_key),
):
    try:
        services.remove_product(sku, uow)
    except services.ProductNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"ok": True}
