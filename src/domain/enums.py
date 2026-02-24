from enum import Enum


class ProductStatus(str, Enum):
    PENDING = "PENDING"
    BOUGHT = "BOUGHT"
    NOT_FOUND = "NOT_FOUND"