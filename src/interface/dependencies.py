from src.application.shared_list import SharedListUseCases
from src.application.product import ProductsUseCases
from src.Infrastructure.db.repository import (
    shared_list,
    product
)

def get_shared_list_usecase():
    repo = shared_list()
    return SharedListUseCases(repo)

def get_products_usecase():
    repo = product()
    return ProductsUseCases(repo)