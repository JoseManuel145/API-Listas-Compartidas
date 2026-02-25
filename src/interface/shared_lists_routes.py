from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

from src.interface.dtos import (
    SharedListCreate,
    SharedListResponse
)
from src.application.shared_list import SharedListUseCases
from src.interface.dependencies import get_shared_list_usecase
from src.domain.models import SharedList

router = APIRouter(prefix="/lists", tags=["Shared Lists"])


@router.get("/", response_model=list[SharedListResponse])
def get_all_lists(
    usecase: SharedListUseCases = Depends(get_shared_list_usecase)
):
    return usecase.get_all_shared_lists()


@router.get("/{list_id}", response_model=SharedListResponse)
def get_list(
    list_id: UUID,
    usecase: SharedListUseCases = Depends(get_shared_list_usecase)
):
    shared_list = usecase.get_shared_list(list_id)
    if not shared_list:
        raise HTTPException(status_code=404, detail="List not found")
    return shared_list


@router.post("/", response_model=SharedListResponse)
def create_list(
    data: SharedListCreate,
    usecase: SharedListUseCases = Depends(get_shared_list_usecase)
):
    shared_list = SharedList(
        id=None,
        name=data.name,
        created_at=None
    )
    return usecase.create_shared_list(shared_list)


@router.put("/{list_id}", response_model=SharedListResponse)
def update_list(
    list_id: UUID,
    data: SharedListCreate,
    usecase: SharedListUseCases = Depends(get_shared_list_usecase)
):
    try:
        shared_list = SharedList(
            id=list_id,
            name=data.name,
            created_at=None
        )
        return usecase.update_shared_list(list_id, shared_list)
    except ValueError:
        raise HTTPException(status_code=404, detail="List not found")


@router.delete("/{list_id}")
def delete_list(
    list_id: UUID,
    usecase: SharedListUseCases = Depends(get_shared_list_usecase)
):
    if not usecase.delete_shared_list(list_id):
        raise HTTPException(status_code=404, detail="List not found")
    return {"deleted": True}