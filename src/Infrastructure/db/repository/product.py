from src.Infrastructure.db.tables.shared_list import SharedListTable
from src.Infrastructure.db.tables.product import ProductTable
from src.domain.enums import ProductStatus
from src.domain.ports import ProductsPort
from sqlalchemy.orm import Session
from src.domain.models import Product
from typing import Optional
from uuid import UUID

class ProductRepository(ProductsPort):
    def __init__(self, session: Session):
        self.session = session
    
    def get_all_products(self) -> list[Product]:
        """Obtener todos los productos"""
        tables = self.session.query(ProductTable).all()
        return [self._to_domain(table) for table in tables]
    
    def get_product(self, product_id: UUID) -> Optional[Product]:
        """Obtener un producto por ID"""
        table = self.session.query(ProductTable).filter(
            ProductTable.id == str(product_id)
        ).first()
        return self._to_domain(table) if table else None
    
    def get_products_by_list(self, list_id: UUID) -> list[Product]:
        """Obtener productos usando el relationship de SharedListTable"""
        shared_list = self.session.query(SharedListTable).filter(
            SharedListTable.id == str(list_id)
        ).first()
        
        if not shared_list:
            return []
        
        return [self._to_domain(producto) for producto in shared_list.productos]
    
    def create_product(self, product: Product) -> Product:
        """Crear un nuevo producto"""
        table = self._to_table(product)
        self.session.add(table)
        self.session.commit()
        self.session.refresh(table)
        return self._to_domain(table)
    
    def update_product(self, product_id: UUID, product: Product) -> Product:
        """Actualizar un producto existente"""
        table = self.session.query(ProductTable).filter(
            ProductTable.id == str(product_id)
        ).first()
        
        if not table:
            raise ValueError(f"Product with id {product_id} not found")
        
        table.list_id = str(product.list_id)
        table.name = product.name
        table.quantity = product.quantity
        table.status = product.status
        table.created_at = product.created_at
        
        self.session.commit()
        self.session.refresh(table)
        return self._to_domain(table)
    
    def delete_product(self, product_id: UUID) -> bool:
        """Eliminar un producto"""
        table = self.session.query(ProductTable).filter(
            ProductTable.id == str(product_id)
        ).first()
        
        if not table:
            return False
        
        self.session.delete(table)
        self.session.commit()
        return True
    
    def update_status(self, product_id: UUID, new_status: str) -> Optional[Product]:
        """Actualizar solo el estado del producto"""
        table = self.session.query(ProductTable).filter(
            ProductTable.id == str(product_id)
        ).first()
        
        if table:
            table.status = new_status
            self.session.commit()
            self.session.refresh(table)
            return self._to_domain(table)
        return None

    def _to_domain(self, table: ProductTable) -> Product:
        """Convertir de tabla a modelo de dominio"""
        # Validamos que el status sea uno de los permitidos
        valid_statuses = ["PENDING", "BOUGHT", "DELETED"]
        status_str = table.status if table.status in valid_statuses else "PENDING"
        
        return Product(
            id=UUID(table.id),
            list_id=UUID(table.list_id),
            name=table.name,
            quantity=table.quantity,
            status=ProductStatus(status_str),
            created_at=table.created_at
        )
    
    from src.Infrastructure.db.tables.shared_list import SharedListTable
from src.Infrastructure.db.tables.product import ProductTable
from src.domain.enums import ProductStatus
from src.domain.ports import ProductsPort
from sqlalchemy.orm import Session
from src.domain.models import Product
from typing import Optional
from uuid import UUID

class ProductRepository(ProductsPort):
    def __init__(self, session: Session):
        self.session = session
    
    def get_all_products(self) -> list[Product]:
        """Obtener todos los productos"""
        tables = self.session.query(ProductTable).all()
        return [self._to_domain(table) for table in tables]
    
    def get_product(self, product_id: UUID) -> Optional[Product]:
        """Obtener un producto por ID"""
        table = self.session.query(ProductTable).filter(
            ProductTable.id == str(product_id)
        ).first()
        return self._to_domain(table) if table else None
    
    def get_products_by_list(self, list_id: UUID) -> list[Product]:
        """Obtener productos usando el relationship de SharedListTable"""
        shared_list = self.session.query(SharedListTable).filter(
            SharedListTable.id == str(list_id)
        ).first()
        
        if not shared_list:
            return []
        
        return [self._to_domain(producto) for producto in shared_list.productos]
    
    def create_product(self, product: Product) -> Product:
        """Crear un nuevo producto"""
        table = self._to_table(product)
        self.session.add(table)
        self.session.commit()
        self.session.refresh(table)
        return self._to_domain(table)
    
    def update_product(self, product_id: UUID, product: Product) -> Product:
        """Actualizar un producto existente"""
        table = self.session.query(ProductTable).filter(
            ProductTable.id == str(product_id)
        ).first()
        
        if not table:
            raise ValueError(f"Product with id {product_id} not found")
        
        table.list_id = str(product.list_id)
        table.name = product.name
        table.quantity = product.quantity
        table.status = product.status
        table.created_at = product.created_at
        
        self.session.commit()
        self.session.refresh(table)
        return self._to_domain(table)
    
    def delete_product(self, product_id: UUID) -> bool:
        """Eliminar un producto"""
        table = self.session.query(ProductTable).filter(
            ProductTable.id == str(product_id)
        ).first()
        
        if not table:
            return False
        
        self.session.delete(table)
        self.session.commit()
        return True
    
    def update_status(self, product_id: UUID, new_status: str) -> Optional[Product]:
        """Actualizar solo el estado del producto"""
        table = self.session.query(ProductTable).filter(
            ProductTable.id == str(product_id)
        ).first()
        
        if table:
            table.status = new_status
            self.session.commit()
            self.session.refresh(table)
            return self._to_domain(table)
        return None

    def _to_domain(self, table: ProductTable) -> Product:
        """Convertir de tabla a modelo de dominio"""
        # Validamos que el status sea uno de los permitidos
        valid_statuses = ["PENDING", "BOUGHT", "DELETED"]
        status_str = table.status if table.status in valid_statuses else "PENDING"
        
        return Product(
            id=UUID(table.id),
            list_id=UUID(table.list_id),
            name=table.name,
            quantity=table.quantity,
            status=ProductStatus(status_str),
            created_at=table.created_at
        )
    
    def _to_table(self, product: Product) -> ProductTable:
        """Convertir de modelo de dominio a tabla"""
        return ProductTable(
            id=str(product.id),
            list_id=str(product.list_id),
            name=product.name,
            quantity=product.quantity,
            status=product.status,
            created_at=product.created_at
        )