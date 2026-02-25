from src.domain.ports import SharedListsPort
from src.domain.models import SharedList
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

class SharedListUseCases:
    def __init__(self, shared_list_port: SharedListsPort):
        self.shared_list_port = shared_list_port

    def get_all_shared_lists(self) -> list[SharedList]:
        return self.shared_list_port.get_all_shared_lists()

    def get_shared_list(self, list_id: UUID) -> Optional[SharedList]:
        return self.shared_list_port.get_shared_list(list_id)

    def create_shared_list(self, shared_list: SharedList) -> SharedList:
        shared_list = SharedList(
            id=uuid4(),
            name=shared_list.name,
            created_at=datetime.now()
        )
        return self.shared_list_port.create_shared_list(shared_list)

    def update_shared_list(self, list_id: UUID, shared_list: SharedList) -> SharedList:
        existing_list = self.shared_list_port.get_shared_list(list_id)
        if not existing_list:
            raise ValueError("Shared list not found")
        shared_list = SharedList(
            id=existing_list.id,
            name=shared_list.name,
            created_at=existing_list.created_at
        )
        return self.shared_list_port.update_shared_list(list_id, shared_list)

    def delete_shared_list(self, list_id: UUID) -> bool:
        return self.shared_list_port.delete_shared_list(list_id)