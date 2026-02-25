from src.Infrastructure.db.db import get_session
from fastapi import Depends
from src.application.shared_list import SharedListUseCases
from src.application.product import ProductsUseCases
from src.Infrastructure.db.repository.shared_list import SharedListRepository
from src.Infrastructure.db.repository.product import ProductRepository


def get_shared_list_usecase(session = Depends(get_session)):
    repo = SharedListRepository(session)
    return SharedListUseCases(repo)

def get_products_usecase(session = Depends(get_session)):
    repo = ProductRepository(session)
    return ProductsUseCases(repo)