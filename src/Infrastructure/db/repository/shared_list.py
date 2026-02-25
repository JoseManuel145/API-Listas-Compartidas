from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session

from src.domain.models import SharedList
from src.domain.ports import SharedListsPort
from src.Infrastructure.db.tables.shared_list import SharedListTable


class SharedListRepository(SharedListsPort):
    def __init__(self, session: Session):
        self.session = session
    
    def get_all_shared_lists(self) -> list[SharedList]:
        """Obtener todas las listas compartidas"""
        tables = self.session.query(SharedListTable).all()
        return [self._to_domain(table) for table in tables]
    
    def get_shared_list(self, list_id: UUID) -> Optional[SharedList]:
        """Obtener una lista compartida por ID"""
        table = self.session.query(SharedListTable).filter(
            SharedListTable.id == str(list_id)
        ).first()
        
        return self._to_domain(table) if table else None
    
    def create_shared_list(self, shared_list: SharedList) -> SharedList:
        """Crear una nueva lista compartida"""
        table = self._to_table(shared_list)
        self.session.add(table)
        self.session.commit()
        self.session.refresh(table)
        return self._to_domain(table)
    
    def update_shared_list(self, list_id: UUID, shared_list: SharedList) -> SharedList:
        """Actualizar una lista compartida existente"""
        table = self.session.query(SharedListTable).filter(
            SharedListTable.id == str(list_id)
        ).first()
        
        if not table:
            raise ValueError(f"SharedList with id {list_id} not found")
        
        table.name = shared_list.name
        table.created_at = shared_list.created_at
        
        self.session.commit()
        self.session.refresh(table)
        return self._to_domain(table)
    
    def delete_shared_list(self, list_id: UUID) -> bool:
        """Eliminar una lista compartida"""
        table = self.session.query(SharedListTable).filter(
            SharedListTable.id == str(list_id)
        ).first()
        
        if not table:
            return False
        
        self.session.delete(table)
        self.session.commit()
        return True
    
    def _to_domain(self, table: SharedListTable) -> SharedList:
        """Convertir de tabla a modelo de dominio"""
        return SharedList(
            id=UUID(table.id),
            name=table.name,
            created_at=table.created_at
        )
    
    def _to_table(self, shared_list: SharedList) -> SharedListTable:
        """Convertir de modelo de dominio a tabla"""
        return SharedListTable(
            id=str(shared_list.id),
            name=shared_list.name,
            created_at=shared_list.created_at
        )