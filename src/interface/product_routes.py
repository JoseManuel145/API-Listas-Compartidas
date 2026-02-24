from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

from src.interface.dtos import (
    ProductCreate,
    ProductResponse
)
from src.application.product import ProductsUseCases
from src.interface.dependencies import get_products_usecase
from domain.models import Product
from src.Infrastructure.db.websocket_manager import manager

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=list[ProductResponse])
def get_all_products(
    usecase: ProductsUseCases = Depends(get_products_usecase)
):
    return usecase.get_all_products()


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: UUID,
    usecase: ProductsUseCases = Depends(get_products_usecase)
):
    try:
        return usecase.get_product(product_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/list/{list_id}", response_model=list[ProductResponse])
def get_products_by_list(
    list_id: UUID,
    usecase: ProductsUseCases = Depends(get_products_usecase)
):
    try:
        return usecase.get_products_by_list(list_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/", response_model=ProductResponse)
async def create_product(
    data: ProductCreate,
    usecase: ProductsUseCases = Depends(get_products_usecase)
):
    product = Product(
        id=None,
        list_id=data.list_id,
        name=data.name,
        quantity=data.quantity,
        status="PENDING",
        created_at=None
    )

    created = usecase.create_product(product)

    products = usecase.get_products_by_list(data.list_id)

    await manager.broadcast(
        data.list_id,
        {
            "type": "LIST_UPDATED",
            "products": products
        }
    )

    return created

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: UUID,
    data: ProductCreate,
    usecase: ProductsUseCases = Depends(get_products_usecase)
):
    product = Product(
        id=product_id,
        list_id=data.list_id,
        name=data.name,
        quantity=data.quantity,
        status="PENDING",
        created_at=None
    )
    updated = usecase.update_product(product_id, product)

    products = usecase.get_products_by_list(data.list_id)

    await manager.broadcast(
        data.list_id,
        {
            "type": "LIST_UPDATED",
            "products": products
        }
    )

    return updated

@router.patch("/{product_id}/status", response_model=ProductResponse)
async def update_product_status(
    product_id: UUID,
    status: str,
    usecase: ProductsUseCases = Depends(get_products_usecase)
):
    try:
        existing_product = usecase.get_product(product_id)

        updated_product = Product(
            id=existing_product.id,
            list_id=existing_product.list_id,
            name=existing_product.name,
            quantity=existing_product.quantity,
            status=status,
            created_at=existing_product.created_at
        )

        updated = usecase.update_product(product_id, updated_product)

        products = usecase.get_products_by_list(existing_product.list_id)

        await manager.broadcast(
            existing_product.list_id,
            {
                "type": "LIST_UPDATED",
                "products": products
            }
        )

        return updated

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.delete("/{product_id}")
async def delete_product(
    product_id: UUID,
    usecase: ProductsUseCases = Depends(get_products_usecase)
):
    existing_product = usecase.get_product(product_id)
    if not usecase.delete_product(product_id):
        raise HTTPException(status_code=404, detail="Product not found")

    products = usecase.get_products_by_list(existing_product.list_id)

    await manager.broadcast(
        existing_product.list_id,
        {
            "type": "LIST_UPDATED",
            "products": products
        }
    )

    return {"deleted": True}