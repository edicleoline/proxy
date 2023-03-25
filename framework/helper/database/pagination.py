from enum import Enum

class PaginateDirection(Enum):
    NEXT     = 'next'
    PREVIOUS = 'previous'

class PaginateOrder(Enum):
    ASC     = 'asc'
    DESC    = 'desc'