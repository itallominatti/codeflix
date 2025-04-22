from uuid import UUID
from dataclasses import dataclass

from app.core.category.domain.category_repository import CategoryRepository



@dataclass
class CategoryOutput:
    id: UUID
    name: str
    description: str
    is_active: bool

@dataclass
class ListCategoryResponse:
    data: list[CategoryOutput]


class ListCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self) -> ListCategoryResponse:
        categories = self.repository.list()

        return ListCategoryResponse(
            data=[
            CategoryOutput(
                id=category.id,
                name=category.name,
                description=category.description,
                is_active=category.is_active
            ) for category in categories
            ]
        )


