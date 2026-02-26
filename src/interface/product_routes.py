from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from src.domain.enums import ProductStatus
from src.interface.dtos import ProductCreate, ProductResponse
from src.application.product import ProductsUseCases
from src.interface.dependencies import get_products_usecase
from src.domain.models import Product
from src.Infrastructure.db.websocket_manager import manager

router = APIRouter(prefix="/products", tags=["Products"])


def serialize_products(products):
    return [
        {
            "id": str(p.id),
            "list_id": str(p.list_id),
            "name": p.name,
            "quantity": p.quantity,
            "status": p.status
        } for p in products
    ]

@router.get("/", response_model=list[ProductResponse])
def get_all_products(usecase: ProductsUseCases = Depends(get_products_usecase)):
    return usecase.get_all_products()

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
            "products": serialize_products(products) 
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
            "products": serialize_products(products) 
        }
    )
    return updated

@router.patch("/{product_id}/status", response_model=ProductResponse)
async def update_product_status(
    product_id: UUID,
    status: ProductStatus,
    usecase: ProductsUseCases = Depends(get_products_usecase)
):
    print(f"Updating product {product_id} status to {status}")
    try:
        existing_product = usecase.get_product(product_id)
        print(f"Existing product: {existing_product} with status {existing_product.status}")
        updated = usecase.update_product_status(product_id, status=status)

        products = usecase.get_products_by_list(existing_product.list_id)
        await manager.broadcast(
            existing_product.list_id,
            {
                "type": "LIST_UPDATED",
                "products": serialize_products(products) 
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
    list_id = existing_product.list_id 
    
    if not usecase.delete_product(product_id):
        raise HTTPException(status_code=404, detail="Product not found")

    products = usecase.get_products_by_list(list_id)
    await manager.broadcast(
        list_id,
        {
            "type": "LIST_UPDATED",
            "products": serialize_products(products) 
        }
    )
    return {"deleted": True}