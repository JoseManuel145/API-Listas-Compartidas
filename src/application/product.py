from src.domain.ports import ProductsPort
from src.domain.models import Product
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime

class ProductsUseCases:
    def __init__(self, products_port: ProductsPort):
        self.products_port = products_port

    def get_all_products(self) -> list[Product]:
        return self.products_port.get_all_products()

    def get_product(self, product_id: UUID) -> Optional[Product]:
        product = self.products_port.get_product(product_id)
        if not product:
            raise ValueError(f"Product with id {product_id} not found")
        return product

    def get_products_by_list(self, list_id: UUID) -> list[Product]:
        """Obtener todos los productos de una lista compartida"""
        products = self.products_port.get_products_by_list(list_id)
        if not products:
            raise ValueError(f"No products found for list {list_id}")
        return products
    
    def create_product(self, product: Product) -> Product:
        product = Product(
            id=uuid4(),
            list_id=product.list_id,
            name=product.name,
            quantity=product.quantity,
            status=product.status, # pendiente, comprado, no encontrado
            created_at=datetime.now()
        )
        return self.products_port.create_product(product)

    def update_product(self, product_id: UUID, product: Product) -> Product:
        existing_product = self.get_product(product_id)
        product = Product(
            id=existing_product.id,
            list_id=existing_product.list_id,
            name=product.name,
            quantity=product.quantity,
            status=product.status,
            created_at=existing_product.created_at
        )
        return self.products_port.update_product(product_id, product)
    
    def update_product_status(self, product_id: UUID, status: str) -> Product:
        existing_product = self.get_product(product_id)
        product = Product(
            id=existing_product.id,
            list_id=existing_product.list_id,
            name=existing_product.name,
            quantity=existing_product.quantity,
            status=status,
            created_at=existing_product.created_at
        )
        return self.products_port.update_product(product_id, product)

    def delete_product(self, product_id: UUID) -> bool:
        return self.products_port.delete_product(product_id)