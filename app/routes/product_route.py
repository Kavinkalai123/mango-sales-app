from fastapi import APIRouter, HTTPException, File, UploadFile, status
from app.config.database import get_database
from app.schema.product_schema import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
)
from app.controllers import product_controller
from app.utils.file_upload import save_upload_file, get_image_url
from typing import List

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=List[ProductResponse])
async def list_products(skip: int = 0, limit: int = 100):
    db = get_database()
    return await product_controller.get_products(db, skip=skip, limit=limit)


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str):
    db = get_database()
    product = await product_controller.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate):
    db = get_database()
    return await product_controller.create_product(db, product)


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(product_id: str, product: ProductUpdate):
    db = get_database()
    updated_product = await product_controller.update_product(db, product_id, product)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product


@router.post("/{product_id}/upload-image", response_model=ProductResponse)
async def upload_product_image(product_id: str, file: UploadFile = File(...)):
    db = get_database()
    saved_filename = await save_upload_file(file)
    image_url = get_image_url(saved_filename)
    updated_product = await product_controller.update_product_image(db, product_id, image_url)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: str):
    db = get_database()
    success = await product_controller.delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")